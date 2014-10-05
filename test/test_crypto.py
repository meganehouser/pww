# coding: utf-8

from pww.crypto import Cipher


def test_plaintext_should_equal_decrypted_text():
    cipher = Cipher(b"password", b"saltlsalt")
    plain = "sample text サンプル テキスト".encode()
    encrypted = cipher.encrypt(plain)
    decrypted = cipher.decrypt(encrypted)

    assert plain == decrypted


def test_different_passwords_should_fail_decryption():
    cipher1 = Cipher(b"password", b"saltsalt")
    cipher2 = Cipher(b"bad password", b"saltsalt")

    plain = "sample text サンプル テキスト".encode()
    encrypted = cipher1.encrypt(plain)
    decrypted = cipher2.decrypt(encrypted)

    assert plain != decrypted


def test_different_salts_should_fail_decryption():
    cipher1 = Cipher(b"password", b"saltsalt")
    cipher2 = Cipher(b"password", b"bad salt")

    plain = "sample text サンプル テキスト".encode()
    encrypted = cipher1.encrypt(plain)
    decrypted = cipher2.decrypt(encrypted)

    assert plain != decrypted
