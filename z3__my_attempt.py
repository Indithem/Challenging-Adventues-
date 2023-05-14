class LogicalError(Exception):
    def __init__(self,*msg):
        # print("A `logical` error was not handled properly! ")
        # print(msg)
        pass

class Rule:
    def __init__(self,condition,implication):

        #shared vars
        self.conditions:dict=condition
        self.implications:dict=implication
    
    def check(self, case):
        """Tries changing all values to match implications whenever conditions are matched.
            Returns True, if there was made any successful change, else False. 
            Carries raised LogicalError if condition was already set but tried to change"""
        to_check = True
        for cond in self.conditions.keys():
            to_check = to_check and case.get_cond(cond)==self.conditions[cond]
        if not to_check:
            return False
        change_made = False
        for cond in self.implications.keys():
            change_made=case.set_case(cond,self.implications[cond]) or change_made
        return change_made

    
class Case:
    """A test case, perhaps, which keeps notes of all the possible scenarios
        Name subject to changes."""

    #shared vars
    independent_vars:list = []
    rules =[]

    def __init__(self,init_vars:dict):
        """If there is any new independent variable, it adds to our -global- list, cleans the given input and makes 
            a new locally accesible variable called conditions"""
        # local vars
        self.conditions:dict = init_vars

        for var in init_vars.keys():
            if var not in self.independent_vars:
                self.independent_vars.append(var)
        for var in self.independent_vars:
            if var not in self.conditions.keys():
                self.conditions[var]=None

    def add_rule(self,rule:Rule):
        self.rules.append(rule)
        for cond in rule.conditions.keys():
            if cond not in self.independent_vars:
                self.independent_vars.append(cond)
        for cond in rule.implications.keys():
            if cond not in self.independent_vars:
                self.independent_vars.append(cond)

    def get_cond(self,cond):
        return self.conditions[cond]

    def get_conds(self):
        return self.conditions
    
    def get_free_conds(self):
        free=[]
        for cond in self.conditions.keys():
            if self.conditions[cond]==None: free.append(cond)
        return free

    def set_case(self,cond,val):
        """returns false if no change was required, else a true, raises exception if case was already fixed"""
        if self.conditions[cond]==None:
            self.conditions[cond]=val
            return True
        else:
            if val!=self.conditions[cond]:
                raise LogicalError(f"Setting case value is mismatched. Can't set {cond} to {val} for the case {self}, it is already {self.conditions[cond]}")
            else: return False   

    def run_rules(self):
        changed:bool = False
        i=0
        n=len(self.rules)
        while i<n:
            changed=self.rules[i].check(self)
            if changed: 
                i=0
            else: i+=1
        
    def print_cases(self):
        for j in self.conditions.values():
            if j==None:
                return None
        print(f"{self}",self.conditions)
                
def find_all_pos(a:Case):
    B=a.get_conds()
    f=a.get_free_conds()

    for i in f:
        B[i]=False    
        try:
            a1=Case(B)
            a1.run_rules()
        except LogicalError as p:
            p=1
        else:
            a1.print_cases()
            find_all_pos(a1)
        del a1

        B[i]=True
        try:
            a1=Case(B)
            a1.run_rules()
        except:
            pass
        else:
            a1.print_cases()
            find_all_pos(a1)

if __name__=="__main__":
    """The club follows six rules:

 - every non-scottish members wear red socks
 - every member wears a kilt or doesn't wear socks
 - the married members don't go out on sunday
 - a member goes out on sunday if and only if he is scottish
 - every member who wears a kilt is scottish and married
 - every scottish member wears a kilt
"""

    c = Case({})
    c.add_rule(Rule({'scottish':False}, {"Red socks":True}))

    # c.add_rule(Rule({'kilt':False}, {"Red socks":False}))
    # c.add_rule(Rule({'Red socks':True}, {"kilt":True}))
    
    c.add_rule(Rule({"married":True}, {"sunday":False}))
    
    c.add_rule(Rule({"scottish":True}, {"sunday":True}))
    c.add_rule(Rule({"scottish":False}, {"sunday":False}))
    c.add_rule(Rule({"sunday":True}, {"scottish":True}))
    c.add_rule(Rule({"sunday":False}, {"scottish":False}))

    # c.add_rule(Rule({"kilt":True}, {"scottish":True,"married":True}))

    c.add_rule(Rule({"scottish":True}, {"kilt":True}))

    # # Finding out all the possibilities
    b={}
    for j in Case.independent_vars:
        b[j]=None
    a=Case(b)
    a.print_cases()
    find_all_pos(a)
