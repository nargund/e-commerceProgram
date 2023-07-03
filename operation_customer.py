from model_user import User
from model_customer import Customer
from operation_user import UserOperation 
import pandas as pd
import re
"""
This class contains customer opertations

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""


class CustomerOperation:

#%%    
    def validate_email(self,user_email:str) -> bool:
        """
        validates email id and returns true or false

        Parameters
        ----------
        user_email : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, user_email):
            return True
        else:
            return False
#%%
    def validate_mobile(self, user_mobile:str) -> bool: 
        """
        validates mobile and returns true or false

        Parameters
        ----------
        user_mobile : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if len(user_mobile) != 10:
            return False
        start_tuple = ("03","04")
        if not user_mobile.startswith(start_tuple):
            return False
        return True
#%%     
    
    def register_customer(
        self, 
        user_name:str,
        user_password:str,
        user_email:str,
        user_mobile:str
    )-> bool:
        """
        registers customer and writes them in file

        Parameters
        ----------
        user_name : str
            DESCRIPTION.
        user_password : str
            DESCRIPTION.
        user_email : str
            DESCRIPTION.
        user_mobile : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        user_oper_obj = UserOperation()
        
        if not (user_oper_obj.check_username_exist(user_name) and 
                user_oper_obj.validate_user_name(user_name) and 
                user_oper_obj.validate_password(user_password) and
                self.validate_email(user_email) and
                self.validate_mobile(user_mobile)
                ):
            #print("inside validation")
            return False
        else:
            user_id = user_oper_obj.generate_unique_user_id()
            user_register_time = user_oper_obj.return_time_str()
            user_password_encyp = user_oper_obj.encrypt_password(user_password)
            customer_obj = Customer(user_id = user_id,
                                    user_name = user_name, 
                                    user_password = user_password_encyp,
                                    user_register_time=user_register_time,
                                    user_email = user_email,
                                    user_mobile = user_mobile
                                    )
            customer_obj_df = pd.DataFrame(customer_obj.__dict__ , index = [0])
            return customer_obj.append_to_file(customer_obj_df,
                                        customer_obj.user_file_path)
            
#%%

    def update_customer(
        self,
        attribute_name: str,
        value: str,
        customer_obj: Customer
    ) -> bool :
        """
        updates customer data and writes data in file

        Parameters
        ----------
        attribute_name : str
            DESCRIPTION.
        value : str
            DESCRIPTION.
        customer_obj : Customer
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        
        
        valid_match_dict = {
            "attribute_match" : [User.user_password,User.user_email,
                                User.user_mobile],
            "validate_method" : ["UserOperation().validate_password",
                      "self.validate_email",
                      "self.validate_mobile"]
                      }
        valid_method_df = pd.DataFrame(valid_match_dict)
        attri_check = valid_method_df.loc[
            valid_method_df["attribute_match"] == attribute_name]
        attri_valid_method_name = (attri_check["validate_method"].item() +
                                   "("+'"'+value+'"'+")")
        
        if not (eval(attri_valid_method_name)) :
            return False
        
        if attribute_name == User.user_password : 
            value = UserOperation().encrypt_password(value)
        
        update_df = User().search_return_df(customer_obj.user_name,
                                          is_user_name=True)
        update_df[attribute_name] = value
        user_file_df = User().read_return_df(customer_obj.user_file_path)
        user_file_df = user_file_df[
            user_file_df[User.user_name]!=customer_obj.user_name].copy()
        
        user_final_df = pd.concat([user_file_df,update_df],ignore_index=True)
        return User().write_df_to_file(user_final_df, User.user_file_path)        
#%%

    def delete_customer(
        self,
        customer_id
    ) -> bool :
        """
        deletes the user with corresponding user_id deletes accordingly else
        returnes false

        Parameters
        ----------
        customer_id : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        curr_user_df = User().search_return_df(customer_id, is_user_name=False,
                                               is_user_id=True)
        if curr_user_df.empty : 
            return False
        else : 
            pass
        
        user_file_df = User().read_return_df(User.user_file_path)
        try: 
            del_file_df = user_file_df[
                user_file_df[User.user_id]!= customer_id].copy()
        except: 
            return False
        else: 
            return User().write_df_to_file(del_file_df, User.user_file_path)
#%% 
    def get_customer_list(
        self,
        page_number: str
    ) -> tuple : 
        """
        creates new customer objects and returns accordingly

        Parameters
        ----------
        page_number : str
            DESCRIPTION.

        Returns
        -------
        tuple
            DESCRIPTION.

        """
        
         
        def create_cust_obj(row) : 
            return Customer(**row["cust_dict"])
        
        page_size = 10
        
        user_file_df = User().read_return_df(User.user_file_path)
        cust_file_df = user_file_df[
            user_file_df[User.user_role] == User.customer_role].copy()
        cust_df_dict = cust_file_df.to_dict("records")
        
        cust_return_df = pd.DataFrame()
        cust_return_df["cust_dict"] = cust_df_dict
        cust_return_df["customer_obj"] = cust_return_df.apply(
            create_cust_obj,axis = 1)
        
        cust_return_df = cust_return_df.drop("cust_dict",axis = 1)
        cust_return_df["page_num"] = (cust_return_df.index//page_size) +1 
        
        final_return_df = cust_return_df[
            cust_return_df["page_num"]== int(page_number)]
        
        return_cust_list = final_return_df["customer_obj"].to_list()
        max_pages = cust_return_df["page_num"].max()
        
        return_tuple = (return_cust_list,page_number,max_pages)
        return return_tuple
        
#%%

    def delete_all_customers(
        self
    ) -> bool :
        
        user_file_df = User().read_return_df(User.user_file_path)
        del_file_df = user_file_df[
            user_file_df[User.user_role] != User.customer_role].copy()
        return User().write_df_to_file(del_file_df, User.user_file_path)
#%%