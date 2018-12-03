{ nixpkgs ? import ./fetchNixpkgs.nix { } }:

rec {
  arduino_with_args = nixpkgs.callPackage ./default.nix { };
}
