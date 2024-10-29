import logging
import datetime
import os


def initLogger(main_file_name: str):
    main_file_name = os.path.splitext(os.path.basename(main_file_name))[0]
    logPath = os.path.join("logs", main_file_name)

    # logフォルダの存在確認
    if not os.path.isdir(logPath):
        # logフォルダの作成
        os.makedirs(logPath)

    now = datetime.datetime.now()
    filename = os.path.join("logs", main_file_name,
                            now.strftime("%Y%m%d") + ".log")
    logging.basicConfig(
        handlers=[
            logging.FileHandler(filename=filename,
                                encoding='utf8', mode='a+')
        ],
        level=logging.DEBUG,
        # format="[%(levelname)s] %(message)s",
        # format='%(asctime)s [%(levelname)s],%(module)s.%(filename)s:%(lineno)d,%(message)s',
        format='%(asctime)s [%(levelname)7s],%(filename)s:%(lineno)d,%(message)s',
        # format='%(asctime)s [%(levelname)7s] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
