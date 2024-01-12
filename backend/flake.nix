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

        deps = pkgs: (with pkgs; [
          python311Full
          python311Packages.pip
          python311Packages.venvShellHook
        ]);
        stdenv = pkgs.stdenv;
      in {
        devShells = {
          dev = pkgs.mkShell {
            venvDir = "./.venv";
            buildInputs = deps(pkgs);
          };
        };
        devShell = self.devShells."${system}".dev;
        
        packages = {
          dockerImage = pkgs.dockerTools.buildImage {
            name = "etebeta-backend";
            # tag = "latest";
            copyToRoot = pkgs.buildEnv {
                name = "foo";
                paths = deps(pkgsLinux) ++ [
                  pkgsLinux.bash 
                  pkgsLinux.coreutils-full 
                ];
                pathsToLink = [ "/bin" ];
            };
          };

          # test = stdenv.mkDerivation {
          #   name = "test";
          #   buildInputs = [ pkgs.bash pkgs.coreutils ];
          #   phases = [ "installPhase" ];
          #   installPhase = ''
          #     mkdir -p $out
          #     echo "hello world" > $out/test.txt
          #   '';
          # };

          default = pkgs.python311Packages.buildPythonPackage {
            pname = "etabeta";
            version = "0.0.1";
            pyproject = true;

            src = ./.;

            nativeBuildInputs = [
              pkgs.python311Packages.setuptools
              pkgs.python311Packages.wheel
            ];

            # has no tests yet
            doCheck = false;
          };
        };

        apps = {
          # run-etabeta = {
          #   type = "app";
          #   program = "${self.packages."${system}".etabeta}/bin/sts";
          # };

          # default = self.apps."${system}".run-etabeta;
        };

      }
   );

}