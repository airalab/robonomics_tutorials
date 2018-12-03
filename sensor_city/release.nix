{ nixpkgs ? import ./fetchNixpkgs.nix { } }:

rec {
  sensor_city = nixpkgs.callPackage ./default.nix { };
}
