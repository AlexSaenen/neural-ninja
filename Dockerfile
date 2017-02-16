from ubuntu:14.04

run apt-get update -y && \
    apt-get install software-properties-common build-essential -y && \
    add-apt-repository ppa:fkrull/deadsnakes -y && \
    add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
    apt-get update -y && \
    apt-get install python3.5 python3-setuptools gcc-4.9 g++-4.9 -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    ln -fs /usr/bin/python3.5 /usr/bin/python3

copy tensorflowWheel/ ./tensorflowWheel/

run easy_install3 pip && \
    pip3.5 --no-cache-dir install \
        checksumdir \
        Cython \
        requests \
        tornado \
        /tensorflowWheel/* && \
    rm -rf /tensorflowWheel && \
    sed -i '1721s/.*/  result_shape.insert(dim[0], 1)/' /usr/local/lib/python3.5/dist-packages/tensorflow/python/ops/array_ops.py

copy src ./app/src/

workdir /app/src

run mkdir -p /app/src/netKit/build && mkdir -p /app/src/neunets

cmd python3.5 -u -B entrypoint.py
