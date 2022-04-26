{
  self,
  nixpkgs,
  flake-utils,
  flake-compat,
}:
flake-utils.lib.eachSystem [
  "aarch64-linux"
  "aarch64-darwin"
  "i686-linux"
  "x86_64-darwin"
  "x86_64-linux"
]
(system: let
  overlays = [];

  pkgs = import nixpkgs {inherit system overlays;};
  name = "nvcheckhealth.py";
  pname = name;
  version = "1.0";
  root = toString ../.;

  ignoreSource = [".git"];
  src = pkgs.nix-gitignore.gitignoreSource ignoreSource root;

  devInputs = [
    pkgs.python3
  ];

  fmtInputs = [
    pkgs.alejandra
    pkgs.black
    pkgs.treefmt
  ];

  meta = with pkgs.lib; {
    homepage = "";
    description = "Work with nvim checkhealh data";
    license = [licenses.mit];
  };
in rec {
  packages.default = with pkgs.python3Packages;
    buildPythonApplication {
      inherit pname src version;
    };
  apps.default = flake-utils.lib.mkApp {drv = packages.default;};

  devShells = {
    default = pkgs.callPackage ./devShell.nix {
      nativeBuildInputs = devInputs ++ fmtInputs;
    };
    fmtShell = pkgs.mkShell {
      name = "fmt-shell";
      nativeBuildInputs = fmtInputs;
    };
  };
})
