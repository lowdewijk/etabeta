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
            name = "etabeta";

            copyToRoot = pkgs.buildEnv {
                name = "foo";

                paths = deps(pkgsLinux) ++ [
                  pkgsLinux.bash 
                  pkgsLinux.coreutils-full
                  pkgsLinux.vim
                  pkgsLinux.findutils
                  pkgsLinux.unzip
                  self.packages."${system}".etabeta
                  self.packages."${system}".etabeta.dist
                ];
                pathsToLink = [ "/bin"  "/" ];
            };

            # ''
            #   #!/bin/bash
            #   python -m venv .venv
            #   source .venv/bin/activate
            #   pip install etabeta-0.0.1-py3-none-any.whl
            # '';

            # python -m venv .venv
            # source .venv/bin/activate
            # pip install etabeta-0.0.1-py3-none-any.whl

          };

          etabeta = pkgs.python311Packages.buildPythonApplication {
            pname = "etabeta";
            version = "0.0.1";
            pyproject = true;

            src = ./.;

            nativeBuildInputs = [
              pkgs.python311Packages.setuptools
              pkgs.python311Packages.setuptools-scm
            ];
          };

          default = self.packages."${system}".etabeta;
        };

      }
   );

}