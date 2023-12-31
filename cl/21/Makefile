CL21=/local/res/stringtruth/cl21

# Things like olivia/train_olivia_a are kaldi train directories.  Move them, they should not be in the repository under the nickname directories.
# for f in ${CL21}/*/train_*; do echo mv ${CL21}/$f kaldi; done


# Directory names corresponding to text files such as /local/res/stringtruth/cl21/mufasa/mufasa_b/text
textfiledir.txt: 
	for n in `cat ${CL21}/nicknames.txt`; do ls -1 ${CL21}/$$n/$$n\_?/text; done | cut -f6-7 -d '/' > textfiledir.txt

cp_textfile: textfiledir.txt
	for d in `cat textfiledir.txt`; do mkdir -p $$d; cp ${CL21}/$$d/text $$d; done


truthfiledir.txt:
	for n in `cat ${CL21}/nicknames.txt`; do ls -1 ${CL21}/$$n/$$n\_?/truth; done | cut -f6-7 -d '/' > truthfiledir.txt


cp_truthfile: truthfiledir.txt
	for d in `cat truthfiledir.txt`; do mkdir -p $$d; cp ${CL21}/$$d/truth $$d; done

wavfiledir.txt: 
	for n in `cat ${CL21}/nicknames.txt`; do ls -d -1 ${CL21}/$$n/$$n\_?/wav; done | cut -f6-7 -d '/' > wavfiledir.txt

wavfile.txt: 
	for n in `cat ${CL21}/nicknames.txt`; do ls -d -1 ${CL21}/$$n/$$n\_?/wav/*.wav; done | cut -f6-9 -d'/'  > wavfile.txt

check_wav:
	for d in `cat wavfiledir.txt`; do for w in `ls $$d/*.wav`; do file $$w; done; done

# It was not necessary to resample
cp_wav: wavfile.txt
	for d in `cat wavfiledir.txt`; do mkdir -p $$d/wav; done
	for w in `cat wavfile.txt` ; do cp ${CL21}/$$w $$w; done

pooled_text:
	cat */*\_?/text > pooled_text

pooled_truth:
	cat */*\_?/truth > pooled_truth






