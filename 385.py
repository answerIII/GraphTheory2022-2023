# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
#class NestedInteger(object):
#    def __init__(self, value=None):
#        """
#        If value is not specified, initializes an empty list.
#        Otherwise initializes a single integer equal to value.
#        """
#
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
#        """
#
#    def add(self, elem):
#        """
#        Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
#        :rtype void
#        """
#
#    def setInteger(self, value):
#        """
#        Set this NestedInteger to hold a single integer equal to value.
#        :rtype void
#        """
#
#    def getInteger(self):
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        :rtype int
#        """
#
#    def getList(self):
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        :rtype List[NestedInteger]
#        """

class Solution(object):
    def deserialize(self, s):
        """
        :type s: str
        :rtype: NestedInteger
        """
        if len(s) == 0:
          return

        if s[0] != '[':
          return NestedInteger(int(s))

        q = []
        number = ''

        for i in range(len(s)):
            if s[i] == '[':
                # q.append(s[i])
                q.append(NestedInteger())
            elif s[i] == ']':
                # temp = []
                # while q[-1] != '[':
                #     temp.insert(0, q.pop())
                # q.pop()
                # q.append(temp)
                temp = q.pop()
                if q:
                    q[-1].add(temp)
                else:
                    return temp

            elif s[i] == ',':
                if number != '':
                    q[-1].add(NestedInteger(int(number)))
                    number = ''
            # if s[i] == '-' or '0' <= s[i] <= '9':
            #     number += s[i]
            # if s[i+1] == ',' or s[i+1] == '[' or s[i+1] == ']':
            #     q.append(int(number))
            #     number = ''
            if s[i] == '-' or '0' <= s[i] <= '9':
                number += s[i]
            if number != '' and (s[i+1] == ',' or s[i+1] == ']'):
                q[-1].add(NestedInteger(int(number)))
                number = ''
           
