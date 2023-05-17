class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        def num(A,me,m):
            if (A==1):
                q=me-1
                w=me+1
            if (A==2):
                q=me-m
                w=me+m
            if (A==3):
                q=me-1
                w=me+m
            if (A==4):
                q=me+1
                w=me+m
            if (A==5):
                q=me-m
                w=me-1
            if (A==6):
                q=me-m
                w=me+1
            return(q,w)
        flag=0
        A=grid
        n=len(A)
        m=len(A[0])
        me=0
        last=0
        while(me!=(n)*(m)-1):
            i=me//m
            j=me%m
            q,w=num(A[i][j],me,m)
            if me==0:
                if (q>0)and(w<=0)and(q<n*m):
                    last=me
                    me=q
                elif (w>0)and(q<=0)and(w<n*m):
                    last=me
                    me=w
                elif (flag==1):
                    last=me
                    me=q
                    flag=0
                elif (w>0)and(q>0):
                    if (w>=n*m):
                        last=me
                        me=q
                    elif (q>=n*m):
                        last=me
                        me=w
                    else:
                        last=me
                        me=w
                        flag=1
                else: return(False)
            elif (q==last):
                if(w<=0)or((i!=w//m)and(j!=w%m))or(w>=n*m): 
                    if flag==0: return(False)
                    last=0
                    me=0
                last=me
                me=w
            elif (w==last):
                if(q<=0)or((i!=q//m)and(j!=q%m))or(q>=n*m):
                    if flag==0: return(False)
                    last=0
                    me=0
                last=me
                me=q
            else: 
                if flag==0: return(False)
                last=0
                me=0
            if (me==(n)*(m)-1):
                q,w=num(A[n-1][m-1],me,m)
                if (q!=last)and(w!=last):
                    if flag==0: return(False)
                    last=0
                    me=0
        return(True)
