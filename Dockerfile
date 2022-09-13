# 
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14
# 
######################################################################################
#	Install AWS CLI
######################################################################################
# install glibc compatibility for alpine
WORKDIR /app

ENV 		GLIBC_VER=2.34-r0
RUN 		apk update
RUN 		apk add tar
RUN 		apk add dos2unix
RUN			apk add coreutils
RUN			apk add py-cryptography
RUN 		apk add gcc musl-dev libffi-dev openssl-dev python3-dev zlib-dev jpeg-dev g++ make swig
RUN 		apk --no-cache add \
				binutils \
				curl \
			&& curl -sL https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub -o /etc/apk/keys/sgerrand.rsa.pub \
			&& curl -sLO https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VER}/glibc-${GLIBC_VER}.apk \
			&& curl -sLO https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VER}/glibc-bin-${GLIBC_VER}.apk \
			&& curl -sLO https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VER}/glibc-i18n-${GLIBC_VER}.apk \
			&& apk add --no-cache \
				glibc-${GLIBC_VER}.apk \
				glibc-bin-${GLIBC_VER}.apk \
				glibc-i18n-${GLIBC_VER}.apk \
			&& /usr/glibc-compat/bin/localedef -i en_US -f UTF-8 en_US.UTF-8 \
			&& curl -sL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip \
			&& unzip awscliv2.zip \
			&& aws/install \
			&& rm -rf \
				awscliv2.zip \
				aws \
				/usr/local/aws-cli/v2/*/dist/aws_completer \
				/usr/local/aws-cli/v2/*/dist/awscli/data/ac.index \
				/usr/local/aws-cli/v2/*/dist/awscli/examples \
				glibc-*.apk \
			&& apk --no-cache del \
				binutils \
				curl \
			&& rm -rf /var/cache/apk/*
# 
COPY ./requirements.txt /app/requirements.txt
#
RUN python -m pip install --upgrade pip
#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
#
COPY app/ /app
# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]