#!encoding=utf-8

import sys
import pathlib
import threading

import srt
from google_trans_new import google_translator


class SrtTranslator:
    def __init__(self, root_dirpath: str = '') -> None:
        self.__root_dirpath = pathlib.Path(root_dirpath)
        if not self.__root_dirpath.exists():
            sys.stderr.write('[error] "{0}" not exists\n'.format(root_dirpath))
            sys.exit(1)
        self.__src_trans_lang = 'en'
        self.__dst_trans_lang = 'ko'
        self.__origin_dirpath = self.__root_dirpath / '_origin_'
        self.__translate_dirpath = self.__root_dirpath / '_translate_'
        self.__srt_filelist = list(self.__root_dirpath.glob('*.srt'))
        if not len(self.__srt_filelist):
            sys.stderr.write('[error] srt file does not exist.\n')
            sys.exit(1)
        self.__init_set()

    def __init_set(self) -> None:
        if not self.__origin_dirpath.exists():
            self.__origin_dirpath.mkdir()
        if not self.__translate_dirpath.exists():
            self.__translate_dirpath.mkdir()

    def multi_translate(self) -> None:
        """
        검색된 모든 srt 자막 파일들 번역
        :return: None
        """
        trans_thread_lst = list()
        for idx, srtfile in enumerate(self.__srt_filelist):
            sys.stdout.write('+++++ {0}: start translating the "{1}" subtitle file. +++++\n'.format(idx+1, srtfile))
            trans_thread = TranslateThread(
                src_file=srtfile, dst_dirpath=self.__translate_dirpath,
                lang_src=self.__src_trans_lang, lang_tgt=self.__dst_trans_lang)
            trans_thread.setDaemon(True)
            trans_thread.start()
            trans_thread_lst.append(trans_thread)
        for trans_thread in trans_thread_lst:
            trans_thread.join()

    def move_to_origin_dir(self) -> None:
        """
        원본 srt 파일 _origin_ 디렉토리로 옮김
        :return: None
        """
        for src_filepath in self.__srt_filelist:
            dst_filepath = self.__origin_dirpath / src_filepath.name
            if dst_filepath.exists():
                dst_filepath.unlink(missing_ok=True)
            src_filepath.rename(dst_filepath)


class TranslateThread(threading.Thread):
    def __init__(self, src_file: pathlib.Path = None, dst_dirpath: pathlib.Path = None,
                 lang_src: str = 'en', lang_tgt: str = 'ko') -> None:
        super(TranslateThread, self).__init__()
        if src_file is None or (not src_file.exists()) or dst_dirpath is None:
            return
        self.__src_file = src_file
        self.__dst_dirpath = dst_dirpath
        self.__lang_src = lang_src
        self.__lang_tgt = lang_tgt
        
    def run(self) -> None:
        """
        번역된 srt 파일 생성
        :return: None
        """
        with self.__src_file.open('rt') as fp:
            file_contents = fp.read()
        google_trans = google_translator()
        subtitles = list()
        for sub in srt.parse(file_contents):
            translated_content = google_trans.translate(
                sub.content, lang_src=self.__lang_src, lang_tgt=self.__lang_tgt)
            tmp_sub = srt.Subtitle(
                index=sub.index, start=sub.start, end=sub.end,
                content=translated_content, proprietary=sub.proprietary)
            sys.stdout.write('{0}: {1}\n'.format(tmp_sub.index, tmp_sub.content))
            subtitles.append(tmp_sub)
        # 번역된 srt 파일 쓰기
        dst_file = self.__dst_dirpath / self.__src_file.name
        with dst_file.open('wt') as fp:
            fp.write(srt.compose(subtitles))


if __name__ == '__main__':
    rdirpath = r'E:\Download'

    srt_trans = SrtTranslator(root_dirpath=rdirpath)
    srt_trans.multi_translate()
    srt_trans.move_to_origin_dir()


