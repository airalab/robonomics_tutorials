{ stdenv
, ros_comm
, mkRosPackage
, python3Packages
, pkgs ? import <nixpkgs> {}
}:

mkRosPackage rec {
  name = "${pname}-${version}";
  pname = "arduino_blink";
  version = "master";

  src = ./.;

  propagatedBuildInputs = with python3Packages;
  [ ros_comm web3 multihash voluptuous ipfsapi pkgs.robonomics_comm ];

  meta = with stdenv.lib; {
    description = "Arduino Blink Lesson";
    homepage = http://github.com/airalab/robonomics_tutorials;
    license = licenses.bsd3;
    maintainers = [ maintainers.vourhey ];
  };
}
