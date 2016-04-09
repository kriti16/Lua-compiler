def check_variable( vari):
        try: 
                int(vari)
                return True
        except ValueError:
                return False
