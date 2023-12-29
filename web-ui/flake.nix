{
  nixConfig.bash-prompt = "etabeta-webui $ ";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let  
        pkgs = import nixpkgs { inherit system; overlays = [ ]; };
        deps = pkgs: (with pkgs; [
          nodejs
          nodePackages.npm
        ]);
      in {
        devShells = {
          dev = pkgs.mkShell {
            buildInputs = deps(pkgs);
          };
        };
        devShell = self.devShells."${system}".dev;
      }
    );
}

