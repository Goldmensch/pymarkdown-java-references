{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = {
    self,
    flake-parts,
    ...
  } @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];

      perSystem = {
        config,
        lib,
        pkgs,
        system,
        ...
      }: {
         devShells.default = pkgs.mkShell {
           name = "PyMarkdown Javadoc references";
           packages = with pkgs; [
                        git
                        python313
                        poetry
           ];
         };
       };
    };
}