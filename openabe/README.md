# Our patch of OpenABE

The file `openabe-patch.diff` is our patch of OpenABE,
to be applied to the current latest version of
[OpenABE](https://github.com/zeutro/openabe).
(commit `b8f9d3c8a2620c1185ca972248f7af39c1eae68c`).
The `openabe` folder contains a copy of OpenABE with this patch applied.

To compile, follow the normal OpenABE installation instructions.
That is, install the dependencies, run `. ./env`,
and then `make all bindings`. If you want it to compile faster, try

```bash
. ./env
make deps
make -j$(nproc) src cli examples bindings
```

You can then test that everything works by e.g. running
```bash
./examples/test_kp
python bindings/python/test.py
```
