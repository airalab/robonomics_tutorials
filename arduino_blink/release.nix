{ nixpkgs ? import ./fetchNixpkgs.nix { } }:

rec {
  arduino_blink = nixpkgs.callPackage ./default.nix { };
}
