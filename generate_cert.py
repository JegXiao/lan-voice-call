from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import socket
import ipaddress  # 新增导入

def generate_self_signed_cert():
    # 1. 生成私钥
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. 获取本机 IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # 3. 构建证书信息
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "LocalDev"),
        x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
    ])

    # 使用 timezone-aware 的 UTC 时间修复警告
    now = datetime.datetime.now(datetime.timezone.utc)

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([
            # 使用 ipaddress 模块修复 TypeError
            x509.IPAddress(ipaddress.IPv4Address(local_ip)),
            x509.DNSName("localhost"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # 4. 保存私钥
    with open("server.key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # 5. 保存证书
    with open("server.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"\n" + "="*30)
    print(f"证书生成成功！")
    print(f"当前局域网 IP: {local_ip}")
    print(f"请确保 server.py 运行在此目录下")
    print("="*30 + "\n")

if __name__ == "__main__":
    generate_self_signed_cert()