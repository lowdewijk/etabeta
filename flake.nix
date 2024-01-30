{
  nixConfig.bash-prompt = "etabeta $(pwd) $ ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; overlays = [ ]; };
        pkgsLinux = import nixpkgs { system = "x86_64-linux"; overlays = [ ]; };
        pythonPkgs = pkgs: pkgs.python311Packages;

        # Backend dependencies
        pythonDeps = pkgs: (with pythonPkgs (pkgs); [
          fastapi
          uvicorn
          openai
          colorlog
          pyyaml
          python-dotenv
        ]);
        pythonBuildDeps = pkgs: (with pythonPkgs (pkgs); [
          build
          mypy
          black
          flake8
          flake8-bugbear
          types-pyyaml
        ]);
        otherBackendDeps = pkgs: (with pkgs; [
          python311Full
        ]);
        backendDeps = pkgs: otherBackendDeps (pkgs) ++ pythonDeps (pkgs) ++ pythonBuildDeps (pkgs);

        # Webui dependencies
        webuiDeps = pkgs: (with pkgs; [
          nodejs
          nodePackages.npm
        ]);

        # All dependencies
        deps = pkgs: (backendDeps pkgs) ++ (webuiDeps pkgs);

        getPropagatedPythonPackages = pkg: (with builtins // pkgs.lib.lists;
          let
            getPropagatedBuildInputs = pkg: pkg.propagatedBuildInputs ++ (map getPropagatedBuildInputs pkg.propagatedBuildInputs);
            pbuilds = unique (flatten ((getPropagatedBuildInputs pkg)));
            result = filter (pkg: (isList (match "^python3.11-.*" pkg.name))) pbuilds;
          in
          result
        );

        # Necessary for the docker image
        getPythonDepsWithPropagatedPackages = pkgs:
          (pythonDeps pkgs) ++ (pkgs.lib.flatten (map getPropagatedPythonPackages (pythonDeps pkgs)));

      in
      {
        devShell = pkgs.mkShell {
          buildInputs = deps (pkgs);
        };

        packages = {
          dockerImage = pkgs.dockerTools.buildImage {
            name = "etabeta";

            copyToRoot = pkgs.buildEnv {
              name = "etabeta-build";

              paths =
                [ self.packages.${system}.backend ] ++
                otherBackendDeps (pkgsLinux) ++
                # These need to be added explicitly for them to be available
                (getPythonDepsWithPropagatedPackages pkgsLinux);

              pathsToLink = [ "/bin" "/lib/python3.11/site-packages" ];
            };

            config = {
              Cmd = [ "python" "-m" "uvicorn" "etabeta.main:app" "--host" "0.0.0.0" ];
              WorkingDir = "/lib/python3.11/site-packages";
            };
          };

          backend = pkgs.python311Packages.buildPythonApplication {
            name = "etabeta-backend";
            
            pyproject = true;
            srcs = [ ./backend self.packages.${system}.webui ];
            sourceRoot = "./backend";

            nativeBuildInputs = (with pythonPkgs (pkgs); [
              setuptools
              setuptools-scm
              mypy
            ]);
            buildInputs = (pythonBuildDeps pkgs) ++ [ self.packages.${system}.webui ];
            propagatedBuildInputs = (pythonDeps pkgs);

            preBuild = ''
              echo Copy webui to static_data
              mkdir -p $PWD/etabeta/static_data/
              cp -rf ${self.packages.${system}.webui}/lib/node_modules/etabeta/dist/* $PWD/etabeta/static_data/
            '';

            checkPhase = ''
              mypy $PWD/etabeta
            '';
          };

          webui = pkgs.buildNpmPackage {
            name = "etabeta-webui";
            src = ./webui;
            npmDepsHash = "sha256-8kTCAY8gUfQR7rvaU1qJghGUf5+lRBrFolznJ3FWHMs=";
            installPhase = ''
              echo Copy dist to lib/node_modules/etabeta
              mkdir -p $out/lib/node_modules/etabeta
              cp -rf $PWD/dist $out/lib/node_modules/etabeta
            '';
          };

          default = self.packages."${system}".dockerImage;
        };

      }
    );

}
