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
      in {
        devShells = {
          dev = pkgs.mkShell {
            venvDir = "./.venv";
            buildInputs = deps(pkgs);
          };
        };
        devShell = self.devShells."${system}".dev;

        apps.test = {
          type = "app";
          program = "<store-path>";
        };

        packages.dockerImage = pkgs.dockerTools.buildImage (builtins.trace "Building docker image" {
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
        });
      }
   );

}