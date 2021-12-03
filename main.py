from services.utils.rbc_parser import rbk_parse

if __name__ == '__main__':
    parser = rbk_parse(2)
    parser.get_text('test.json')
    print(parser.data_to_write)
