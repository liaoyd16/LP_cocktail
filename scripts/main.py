
import sys
sys.path.append("../")
sys.path.append("../TIMIT_proc")
import Meta
import prepare_doc_jsons
import do_gender_sp
import do_sp_sent
import do_phone_sentdur
import do_phone_gender_sentdur
import do_phone_gender_pair
import do_phone_gender_vals

def main():
    # TIMIT_proc
    """ doc jsons """
    # prepare_doc_jsons.do_speaker_info()
    # prepare_doc_jsons.input_phones()
    """ table jsons """
    # do_gender_sp.do_gender_sp()
    # do_sp_sent.do_sp_sent()
    # do_phone_sentdur.do_phone_sentdur()
    # do_phone_gender_sentdur.do_phone_gender_sentdur()
    # do_phone_gender_pair.do_phone_gender_pair()
    """ scripts """
    do_phone_gender_vals.do_phone_gender_vals()
    # display.display()

if __name__ == '__main__':
    main()