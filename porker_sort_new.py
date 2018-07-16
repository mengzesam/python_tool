import math

class porker():
    porker_dict={0:'A',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',
                 7: '8',8:'9',9:'10',10:'J',11:'Q',12:'K'}
    def __init__(self,N):
        self.seq_size=N

    def transform(self,seq_in):
        if(type(seq_in)!=list):
            return
        N=len(seq_in)
        if(N<1):
            return
        seq_out=[]
        step=2
        offset=0
        next_first=-offset+1
        index=offset
        NUM=N
        while NUM>0:
            while index>=0 and index<N:
                seq_out.append(seq_in[index])
                index=index+step
            M=int((NUM+offset)/2)
            offset=(NUM+offset)%2
            NUM=M
            if offset==0:
                index=next_first
                next_first=next_first+step
            elif offset==1:
                if NUM==1:
                    index=next_first
                else:
                    index=next_first+step
            step=2*step
        return seq_out

    def normalize(self):
        self.sequence=range(self.seq_size)
        tmp_seq=self.transform(self.sequence)
        for i in range(self.seq_size):
             self.sequence[tmp_seq[i]]=i

    def display(self):
        out_ss=''
        for i in self.sequence:
            out_ss=out_ss+self.porker_dict[i]+' '
        print  out_ss



if __name__=='__main__':
    porker=porker(13)
    porker.normalize()
    porker.display()
