#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>

using namespace std;

enum State : bool
{
	Undefined = 0,
	Bad = 1
};

class Solution {
public:
	bool pyramidTransition(string bottom, vector<string>& allowed) 
	{
		if (allowed.size() == 0)
		{
			return false;
		}

		for (string Tree : allowed)
		{
			Threes[Tree.substr(0, 2)].push_back(Tree[2]);
		}
		return pyramidTransitionDFS(bottom, "");
	}

private:
	bool pyramidTransitionDFS(string Bottom, string Top)
	{
		// Проверяем верх ли это
		if (Bottom.size() == 2 && Top.size() == 1)
		{
			return true;
		}

		// Проверяем можно ли переходить на следующий уровень
		if (Bottom.size() == Top.size() + 1)
		{
			if (BadWords[Top] == State::Bad)
			{
				return false;
			}
			bool Result = pyramidTransitionDFS(Top, "");
			BadWords[Top] = State::Bad;
			return Result;

		}

		string Substring = Bottom.substr(Top.size(), 2);

		// Есть ли вообще тройка с такой двойкой внизу?
		if (Threes.count(Substring) == 0)
		{
			return false;
		}

		//Добавляем буквы в Top и запускаем DFS 
		for (char UpLetter : Threes[Substring])
		{
			if (pyramidTransitionDFS(Bottom, Top + UpLetter))
			{
				return true;
			}
		}
		return false;
	}
	unordered_map<string, State> BadWords;
	unordered_map<string, vector<char>> Threes;
};


int main()
{
	string bottom = "DBCDA";
	vector<string> allowed = { "DBD","BCC","CDD","DAD","DDA","AAC","CCA","BCD" };

	Solution sol;
	cout << sol.pyramidTransition(bottom, allowed);
}

