FROM odoo:19.0

USER root

# 配置 apt 使用 163 镜像源
RUN if [ -f /etc/apt/sources.list ]; then \
        sed -i 's/deb.debian.org/mirrors.163.com/g' /etc/apt/sources.list; \
    fi && \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/deb.debian.org/mirrors.163.com/g' /etc/apt/sources.list.d/debian.sources; \
    fi

# 安装 PostGIS 客户端依赖和常用工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-16 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 安装项目所需的额外的 Python 库，使用清华大学的 PyPI 镜像源 (更加稳定)
RUN pip3 install --no-cache-dir --break-system-packages \
    -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn \
    --retries 10 \
    jsonpath-ng \
    numpy \
    scipy \
    requests \
    jinja2 \
    paho-mqtt

USER odoo
