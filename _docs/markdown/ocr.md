

# 참조 사이트
- [Git: tesstrain](https://github.com/tesseract-ocr/tesstrain)

- [Training your tesseract on windows 10](https://medium.com/@gaopengbai0121/training-your-tesseract-on-windows-10-df6756946d4f)
- [Simple OCR with Tesseract](https://towardsdatascience.com/simple-ocr-with-tesseract-a4341e4564b6)

- [A comprehensive guide to OCR with Tesseract, OpenCV and Python](https://nanonets.com/blog/ocr-with-tesseract/)


- [jTessBoxEditor](http://vietocr.sourceforge.net/training.html)

- [JTessBoxEditor로 이미지 인식하기](https://hello-gg.tistory.com/5)
- [png or jpeg -> tif -> box 변환하기](https://hello-gg.tistory.com/6)

- [Tesseract OCR 4.0 학습](https://m.blog.naver.com/jerry1455/221412511622)
- [Tesseract OCR4 한글 학습하기](https://diyworld.tistory.com/114)


# 설치 및 환경 변수 편집

## tesseract-ocr
- [Tesseract로 OCR 하기](https://joyhong.tistory.com/79)
- [UB-Mannheim tesseract](https://github.com/UB-Mannheim/tesseract/wiki)


## java
- [Java Runtime Environment]()
- [Java SE Downloads](https://www.oracle.com/java/technologies/javase-downloads.html)
- [자바(JAVA) JDK 설치 및 환경 변수 설정하는 방법](https://prolite.tistory.com/975)


## jTessBoxEditor
- [jTessBoxEditor Download](https://sourceforge.net/projects/vietocr/files/jTessBoxEditor/)


# 


https://towardsdatascience.com/simple-ocr-with-tesseract-a4341e4564b6


C:\Program Files\Tesseract-OCR

num.rok.exp0.tif
C:\Dev\docMoon\trainings\ocr> tesseract num.rok.exp0.tif num.rok.exp0 batch.nochop makebox

<!-- tesseract num.rok.exp0.tif num.rok.exp0 batch.nochop makebox -->

tesseract --psm 6 --oem 3 num.rok.exp0.tif num.rok.exp0 makebox


echo rok 0 0 0 0 0 > font_properties

tesseract num.rok.exp0.tif num.rok.exp0 batch.nochop makebox


tesseract.exe num.rok.exp0.tif num.rok.exp0 nobatch box.train
shapeclustering -F font_properties -U unicharset -O num.unicharset num.rok.exp0.tr
mftraining -F font_properties -U unicharset -O num.unicharset num.rok.exp0.tr
cntraining.exe num.rok.exp0.tr
rename normproto num.normproto 
rename inttemp num.inttemp 
rename pffmtable num.pffmtable 
rename shapetable num.shapetable 
combine_tessdata.exe num.




환경 변수
TESSDATA_PREFIX C:\Program Files\Tesseract-OCR\tessdata

num.traineddata 복사 -> C:\Program Files\Tesseract-OCR\tessdata


C:\Dev\docMoon\trainings\ocr> tesseract main_top_power01.png stdout -l num


tesseract moreinfo01.png stdout -l num

tesseract moreinfo_power4.png stdout -l num