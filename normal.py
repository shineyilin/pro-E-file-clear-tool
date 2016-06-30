import os
import sys
import __builtin__
import string
from dircache import listdir

print os.getcwdu();
s=os.sep
#root='D:'+s+'Program Files'+s+'start_dir'+s+'purge'+s #adress in file name
root=os.getcwdu()+'\\';
file_bef=file('u1.txt', 'w+'); 
file_end=file('u2.txt', 'w+'); 
file_all=file('u3.txt', 'w+');  
def is_ptcfile( word ):#find if the word is belong to tc file type
    l=len(word);
    if l <4:
        return False;
    ftype=word[l-3]+word[l-2]+word[l-1];
    if  ftype == 'asm' or ftype == 'prt' or ftype=='win':    
        return True;
    return False;

def is_ptcotherfile(word):
    l=len(word);
    if l <5:
        return False;
    fty=word[l-3]+word[l-2]+word[l-1];
    ft=word[0]+word[1]+word[2]+word[3]+word[4];
    if  fty == 'log' or fty == 'inf' or fty == 'log' or ft == 'trail':    
        return True;
     
    return False;

def file_end_version (word):#to delay the point in version
    l=len(word);
    a=0;
    for i in range(1,l):
        a*=10;
        a+=int( word[i] );
    file_end.write(str(a)+'\n');
    return 0;

g_all=0; 


for f in listdir(root):
    if os.path.isfile(os.path.join(root,f)):
        fname = os.path.splitext(f);
        if  is_ptcfile( fname[0] ) == True:
            name=fname[0]+fname[1];
            newname=fname[0]+'.1';
            if  is_ptcfile( fname[0] ) == True:
                file_bef.write(fname[0]+'\n');
                file_end_version(fname[1]   );
                file_all.write(name+    '\n');
                g_all+=1;


      
print "total file is: " +str(g_all);

file_all.seek(0);
file_bef.seek(0);
file_end.seek(0);

offset =0;
offset1=0;
offset2=0;

finish_p=0;
while True:
    file_all.seek(offset  );
    file_bef.seek(offset1 );
    file_end.seek(offset2 );

    word   = file_all.readline();
    word1  = file_bef.readline();
    word2  = file_end.readline();
    
    offset = file_all.tell();
    offset1= file_bef.tell();
    offset2= file_end.tell();
    length = len(word); 
    if  length==0:
        break;
    if word[0] != '.':
        for i in range(0,g_all):
            tex_word  =  file_all.readline();
            tex_word1 =  file_bef.readline();
            tex_word2 =  file_end.readline();
            if  len(tex_word) == 0:
                break;
            if  tex_word[0] != '.':
                if string.upper(word1) == string.upper( tex_word1 ):
                    if  int(tex_word2) < int(word2):
                        ch_offset = file_all.tell();
                        ch_word   = tex_word;
                    else:
                        ch_offset = offset;
                        ch_word   = word;
                    ch_length=len(ch_word);
                    word=ch_word;
                    ch_word=string.replace(ch_word,'\n','');
                    #os.rename(root,root);
                    os.remove(root+ch_word);
                    print 'DEL: '+ch_word;
                    finish_p+=1;
                    file_all.seek(ch_offset-ch_length-1);#have down mark
                    file_all.write('..');
                    file_all.seek(offset)
                    break;
                    
    if word[0]!='0':
        file_all.seek(offset-length-1);#have down mark
        file_all.write('.');         
print 'process file number is: '+str(finish_p); 

for f in listdir(root):
    if os.path.isfile(os.path.join(root,f)):
        fname = os.path.splitext(f);
        if  is_ptcfile( fname[0] ) == True:
            newname=fname[0]+'.1';
            #print f;
            #print newname;
            os.rename( root+f , root+newname );
        if  is_ptcotherfile(fname[0])==True:
            os.remove(root+f);
            
file_bef.close();
file_end.close();
file_all.close();

os.remove(root+'u1.txt');
os.remove(root+'u2.txt');
os.remove(root+'u3.txt');
raw_input('sucess finish!!!\npress any key to continue !')

