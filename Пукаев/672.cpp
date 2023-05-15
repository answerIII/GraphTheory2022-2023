class Solution {
public:
    int flipLights(int n, int presses) {
        if(presses){
            set<string> result;
            string lights(n, '1');
            unordered_map<string,unordered_map<int,int>>lightsToStep;
            DFS(lights, 0, presses, result, lightsToStep);
            return result.size();
        }
        else{
            return 1;
        }
    }

    void DFS(string lights, int pressed, int presses, set<string>& result, unordered_map<string,unordered_map<int,int>>& lightsToStep){
        if( pressed == presses){
            result.insert(lights);
            return;
        }
        
        if(lightsToStep.count(lights) and lightsToStep[lights].count(pressed)) return;
        lightsToStep[lights][pressed] = 1;
        
        string lights1 = pressButton1(lights);
        string lights2 = pressButton2(lights);
        string lights3 = pressButton3(lights);
        string lights4 = pressButton4(lights);
        
        DFS(lights1, pressed+1, presses, result, lightsToStep);
        DFS(lights2, pressed+1, presses, result, lightsToStep);
        DFS(lights3, pressed+1, presses, result, lightsToStep);
        DFS(lights4, pressed+1, presses, result, lightsToStep);
        return;
    }

    string pressButton1(string light){
        string lights = light;
        for(int i=0; i<lights.size(); i++){
            if(lights[i] == '1') lights[i] = '0';
            else lights[i] = '1';
        }
        return lights;
    }
    string pressButton2(string light){
        string lights = light;
        for(int i=0; i<lights.size(); i+=2){
            if(lights[i] == '1') lights[i] = '0';
            else lights[i] = '1';
        }
        return lights;
    }
    string pressButton3(string light){
        string lights = light;
        for(int i=1; i<lights.size(); i+=2){
            if(lights[i] == '1') lights[i] = '0';
            else lights[i] = '1';
        }
        return lights;
    }
    string pressButton4(string light){
        string lights = light;
        for(int i=0; i<lights.size(); i = i*3+1){
            if(lights[i] == '1') lights[i] = '0';
            else lights[i] = '1';
        }
        return lights;
    }
};