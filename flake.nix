{
  nixConfig.bash-prompt = "etabeta $ ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let  
        pkgs = import nixpkgs { inherit system; overlays = [ ]; };
        deps = pkgs: (with pkgs; [
          nodejs
          nodePackages.npm
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
      }
    );
}

