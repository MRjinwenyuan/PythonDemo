


if __name__ == '__main__':
    try:
        print('try')
        r = 10 / 0
        print(r)
    except Exception as e:
        print(e)
    finally:
        print('finally')

    print('end')