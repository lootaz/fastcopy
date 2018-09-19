#include "Python.h"
#include "fastcopy.h"

static char py_copy_doc[] = "Fast copy from src to dst";
static PyObject *
py_fastcopy(PyObject *self, PyObject *args) {
    char *src;
    char *dst;
    long long inFileSize;
    if(!PyArg_ParseTuple(args, "ss", &src, &dst))
        return NULL;

    fastcopy(src, dst);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef _fastcopymethods[] = {
    {"fastcopy", py_fastcopy, METH_VARARGS, py_copy_doc},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION < 3
void init_fastcopy(void) {
    PyObject *mod;
    mod = Py_InitModule("_fast_copy", _fastcopymethods);
}
#else
static struct PyModuleDef _fastcopymodule = {
    PyModuleDef_HEAD_INIT,
    "_fastcopy",
    NULL,
    -1,
    _fastcopymethods
};

PyMODINIT_FUNC
PyInit__fastcopy(void) {
    PyObject *mod;
    mod = PyModule_Create(&_fastcopymodule);
    return mod;
}
#endif