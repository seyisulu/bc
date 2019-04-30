from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = (
    b'gAAAAABcoQcqO8fi1grNAXpZF7jQaMeB87zdH8ZW9CTSbFqBF94bUsx2OfqCXXiU_pc795u'
    b'L4Cce4yUhEEt4ZTAOn9X-ItDntV7U3FjfQctfMEpZla7ymvq8rmYR-o_YlxKGukS7s7AT7F'
    b'-H7W3fmzOIgVHLRg5uI3lzvNrQbUrzibZuDa2ho6k=')


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()

