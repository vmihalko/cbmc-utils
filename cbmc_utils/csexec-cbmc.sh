#!/usr/bin/bash

usage() {
  cat << EOF
USAGE:
1) export PATH=\$(cswrap --print-path-to-wrap):\$PATH'
2) export CSWRAP_ADD_CFLAGS=-Wl,--dynamic-linker,/usr/bin/csexec-loader
3) Build the source with 'goto-clang' 
4) CSEXEC_WRAP_CMD=$'csexec-cbmc\a--unwind\a1' make check
EOF
}

if [ $# -eq 0 ]; then
  usage
  exit 1
fi

i=1
while [ ! -e ${!i} ]; do
  echo "${!i}" 
  CBMC_ARGS[$i - 1]="${!i}"
  ((i++))
done

# Skip LD_LINUX_SO
((i++))

# Skip "--preload libcsexec-preload.so"
((i += 2))

# Skip --argv0
if [ "${!i}" = "--argv0" ]; then
  ((i += 2))
fi

BINARY="${!i}"
((i++))

BINARY_ARGV="${!i}"
((i++))

while [ "$i" -le $# ]; do
  BINARY_ARGV="$BINARY_ARGV,${!i}"
  ((i++))
done

echo "Executing 'cbmc ${CBMC_ARGS[*]} $BINARY'" 1> /dev/tty 2>&1
cbmc "${CBMC_ARGS[@]}" "$BINARY" 1> /dev/tty 2>&1

i=1
while [[ ! "${!i}" =~ "ld-linux" ]]; do
    ((i++))
done

ARGS=( "$@" )
exec "${ARGS[@]:i-1}"
