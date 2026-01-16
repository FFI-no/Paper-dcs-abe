{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = with pkgs; [
      # Compiling
      virtualenv
      bison
      gtest
      flex
      unzip
      gmpxx
      cmake
      wget
      m4
      autoconf
      gcc

      (python3.withPackages (ps: with ps; [
        numpy
        pip

        # For making the python bindings (without the venv)
        setuptools
        cython
      ]))

    ];

    # Nix has an option to protect against build impurities caused by
    # -march=native, but we want them.
    shellHook = ''
      export NIX_ENFORCE_NO_NATIVE=0
    '';
}
