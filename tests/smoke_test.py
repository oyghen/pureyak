import pureyak


def main():
    actual = pureyak.__name__
    expected = "pureyak"
    if actual == expected:
        print("smoke test passed")
    else:
        raise RuntimeError("smoke test failed")


if __name__ == "__main__":
    main()
