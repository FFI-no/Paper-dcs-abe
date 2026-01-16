{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = with pkgs; [
      protobuf
      (python3.withPackages (ps: with ps; [ protobuf ]))
    ];
}
