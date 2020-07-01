import numpy as np

def Jacobi(A,n): #A为nxn对称矩阵，求对称矩阵特征值，返回1xn数组保存特征值    
    if(n==1):
        ans=[0]
        ans[0]=A[0,0]
        return ans
    AA=np.zeros(int(n*(n+1)/2))
    for k in range(n):#根据对称矩阵A特点，AA为一维数组只保存A矩阵上三角元素（包括对角元素），0至n-1保存对角元素
        AA[k]=A[k,k]
    k=n
    for r in range(n-1):#AA的第n个元素开始保存上三角非对角元素
        for c in range(r+1,n):
            AA[k]=A[r,c]
            k=k+1
    air_old=np.zeros(n)
    k=n
    idx=n #非对角最大元素index
    i=0
    j=1
    for r in range(n-1):
        for c in range(r+1,n):
            if(abs(AA[k])>abs(AA[idx])):
                idx=k
                i=r
                j=c
            k=k+1  
    eps=1e-8
    itera=0
    while(abs(AA[idx])>eps and itera<100): 
        itera=itera+1
        theta=np.arctan2(2*AA[idx],(AA[i]-AA[j]))/2
        cos=np.cos(theta)
        sin=np.sin(theta)
        aij=AA[idx]
        aii=AA[i]
        ajj=AA[j]
        rs=int(n+i*n-i*(i+1)/2)  #rs为上三角每一行（第1至第n-1行）第一个元素在AA中的index
        kk=0
        for k in range(rs,rs+j-i-1):#先保存aij行元素，j>i
            air_old[kk]=AA[k]
            kk=kk+1
        for k in range(rs+j-i,rs+n-i-1):
            air_old[kk]=AA[k]
            kk=kk+1
        for r in range(i): #计算1至i-1行i列和j列
            rs=int(n+r*n-r*(r+1)/2)
            ari=AA[rs+i-r-1]
            arj=AA[rs+j-r-1]
            AA[rs+i-r-1]=ari*cos+arj*sin
            AA[rs+j-r-1]=-ari*sin+arj*cos
        for c in range(i+1,j): #计算i行i+1列至j-1列
            rs=int(n+i*n-i*(i+1)/2)
            rsc=int(n+c*n-c*(c+1)/2)
            AA[rs+c-i-1]=AA[rs+c-i-1]*cos+AA[rsc+j-c-1]*sin
        for c in range(j+1,n):#计算i行j+1列至n列
            rs=int(n+i*n-i*(i+1)/2)
            rsj=int(n+j*n-j*(j+1)/2)
            AA[rs+c-i-1]=AA[rs+c-i-1]*cos+AA[rsj+c-j-1]*sin
        k=0
        for r in range(i+1,j):#计算i+1行至j-1行j列
            rs=int(n+r*n-r*(r+1)/2)
            AA[rs+j-r-1]=-air_old[k]*sin+AA[rs+j-r-1]*cos
            k=k+1
        for c in range(j+1,n):#计算j行j+1列至n列
            rs=int(n+j*n-j*(j+1)/2)
            AA[rs+c-j-1]=-air_old[k]*sin+AA[rs+c-j-1]*cos
            k=k+1
        AA[idx]=0
        AA[i]=aii*cos*cos+ajj*sin*sin+2*aij*cos*sin
        AA[j]=aii*sin*sin+ajj*cos*cos-2*aij*cos*sin
        k=n
        idx=n
        i=0
        j=1
        for r in range(n-1):
            for c in range(r+1,n):
                if(abs(AA[k])>abs(AA[idx])):
                    idx=k
                    i=r
                    j=c
                k=k+1 
    #print('itera',itera)
    ans=np.zeros(n)
    for k in range(n):
        ans[k]=AA[k]
    return ans


if __name__ == "__main__":
    #A=np.array([3.5,-6,5,-6,8.5,-9,5,-9,8.5]).reshape(3,3)
    #A=np.array([1,2**0.5,2,2**0.5,3,2**0.5,2,2**0.5,1]).reshape(3,3)
    #A=np.array([3,1,0,1,4,2,0,2,1]).reshape(3,3)
    #A=np.array([4,2,0,0,0,2,4,2,0,0,0,2,4,2,0,0,0,2,4,2,0,0,0,2,4]).reshape(5,5)
    A=np.array([2,4,4,3]).reshape(2,2)
    #A=np.array([1]).reshape(1,1)
    n,_=A.shape
    print('A=\n',A,'\n')
    print('Jacobi方法特征值:\n',Jacobi(A,n),'\n')
    eigs,_=np.linalg.eig(A)
    print('numpy计算特征值:\n',eigs,'\n')