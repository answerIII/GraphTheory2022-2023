class Solution:
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        A=grid
        n=len(A)
        m=len(A[0])
        pos=[[0]*2 for _ in range(8)]
        me=0
        q=0
        w=0
        if A[0][0]!=0:return(False)
        while (me!=n*m-1):
            pos[0][0]=q-2
            pos[0][1]=w+1
            pos[1][0]=q-1
            pos[1][1]=w+2
            pos[2][0]=q+1
            pos[2][1]=w+2
            pos[3][0]=q+2
            pos[3][1]=w+1
            pos[4][0]=q+2
            pos[4][1]=w-1
            pos[5][0]=q+1
            pos[5][1]=w-2
            pos[6][0]=q-1
            pos[6][1]=w-2
            pos[7][0]=q-2
            pos[7][1]=w-1
            i=0
            while (i<8):
                x=pos[i][0]
                y=pos[i][1]
                if (x>=0)and(x<n)and(y>=0)and(y<m):
                    if (A[x][y]==me+1):
                        me+=1
                        i=10
                        q=x
                        w=y
                i+=1
            if i<10:return(False)
        return(True)
