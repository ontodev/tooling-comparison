FROM obolibrary/odkfull:v1.2.28
LABEL maintainer="james@overton.ca"

# Install Ubuntu packages
RUN apt-get install -y \
    libssl-dev \
    raptor2-utils \
    time

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="${PATH}:/root/.cargo/bin/"

# Install horned-owl (requires libssl-dev)
RUN git clone https://github.com/phillord/horned-owl.git && \
    cd horned-owl && \
    cargo build --release
ENV PATH="${PATH}:/tools/horned-owl/target/release/"

# Install RDFTab
ENV RDFTAB_THIN 0.1.1
RUN curl -L -o rdftab-thin https://github.com/ontodev/rdftab.rs/releases/download/v${RDFTAB_THIN}/rdftab-x86_64-unknown-linux-musl && \
    chmod +x rdftab-thin

# Install Python packages
COPY requirements.txt /tools/tooling-comparison-requirements.txt
RUN pip install -r /tools/tooling-comparison-requirements.txt

# Run the tooling comparison
CMD python -u src/run.py
