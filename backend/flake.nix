{
  nixConfig.bash-prompt = "etabeta-backend $ ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let  
        pkgs = import nixpkgs { inherit system; overlays = [ ]; };
        pkgsLinux = import nixpkgs { system = "x86_64-linux";  overlays = [ ]; };
        pythonPkgs = pkgs: pkgs.python311Packages;

        pythonDeps = pkgs: (with pythonPkgs(pkgs); [
          fastapi
          uvicorn
          openai
          colorlog
          pyyaml
          python-dotenv
        ]);
        pythonBuildDeps = pkgs: (with pythonPkgs(pkgs); [
          build
          mypy
          black
          flake8
          flake8-bugbear
          types-pyyaml
        ]);
        otherDeps = pkgs: (with pkgs; [
          python311Full
        ]);
        deps = otherDeps(pkgs) ++ pythonDeps(pkgs) ++ pythonBuildDeps(pkgs);
        
        stdenv = pkgs.stdenv;

        getPropagatedPythonPackages = pkg: (with builtins // pkgs.lib.lists;
          let 
            getPropagatedBuildInputs = pkg: pkg.propagatedBuildInputs ++ (map getPropagatedBuildInputs pkg.propagatedBuildInputs);
            pbuilds = unique ( flatten ( (getPropagatedBuildInputs pkg ) ));
          in 
            #FIXME use builtins.elem
            filter (pkg: (isList (match "^python3.11-.*" pkg.name))) pbuilds);

      in {
        devShell = pkgs.mkShell {
          buildInputs = deps(pkgs);
        };
        
        packages = {
          dockerImage = pkgs.dockerTools.buildImage {
            name = "etabeta";

            copyToRoot = pkgs.buildEnv {
                name = "etabeta-build";

                paths = [
                  pkgsLinux.bash 
                  pkgsLinux.coreutils-full
                  pkgsLinux.vim
                  pkgsLinux.curl
                  pkgsLinux.findutils
                  pkgsLinux.unzip
                  self.packages."${system}".etabeta                  
                  pkgsLinux.python311Full
                ] ++ getPropagatedPythonPackages self.packages."${system}".etabeta;
                pathsToLink = [ "/bin"  "/" ];
            };

            config = { 
              Entrypoint = [ "python" "-m" "uvicorn" "etabeta.main:app" "--host" "0.0.0.0" ];
              WorkingDir = "/lib/python3.11/site-packages";
              ExposedPorts = { "8000/tcp" = {}; };
            };
          };

          etabeta = pkgs.python311Packages.buildPythonApplication {
            pname = "etabeta";
            version = "0.0.1";
            pyproject = true;

            src = ./.;

            nativeBuildInputs = (with pythonPkgs(pkgs); [
              setuptools
              setuptools-scm
              mypy
            ]);

            buildInputs = pythonBuildDeps(pkgs);
            propagatedBuildInputs = pythonDeps(pkgs);
            checkPhase = ''
              runHook preCheck
              mypy $src
              runHook postCheck
            '';
          };

          default = self.packages."${system}".etabeta;
        };

      }
   );

}