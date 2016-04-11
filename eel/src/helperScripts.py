def check_variable( vari):
        try:
                if vari[0] == 't':
                        return False
                else:
                        raise Exception
        except:
                #print(vari)
                return True
                
        
