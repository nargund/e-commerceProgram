from model_user import User
from model_admin import Admin
from operation_user import UserOperation 
from operation_customer import CustomerOperation
from model_customer import Customer
import pandas as pd
import re

"""
This class contains customer opertations

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""


class AdminOperation:
    
    def register_admin(
        self, 
        user_name:str,
        user_password:str,
        is_super_admin: bool = False
    )-> bool:
        """
        creates admin both super and normal

        Parameters
        ----------
        user_name : str
            DESCRIPTION.
        user_password : str
            DESCRIPTION.
        is_super_admin : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        # all variables are validated and follows rules
        #create a customer instance 
        
        user_oper_obj = UserOperation()
        
        if not (user_oper_obj.check_username_exist(user_name) and 
                user_oper_obj.validate_user_name(user_name) and 
                user_oper_obj.validate_password(user_password)
                ):
            return False
        else:
            user_id = user_oper_obj.generate_unique_user_id()
            user_register_time = user_oper_obj.return_time_str()
            user_password_encyp = user_oper_obj.encrypt_password(user_password)
            if is_super_admin :
                user_role = Admin.super_admin_role
            else: 
                user_role = Admin.admin_role
                
            new_admin_obj = Admin(user_id = user_id,
                                  user_name = user_name, 
                                  user_password = user_password_encyp,
                                  user_register_time=user_register_time,
                                  user_role = user_role
                                  )
            admin_obj_df = pd.DataFrame(new_admin_obj.__dict__ , index = [0])
            return new_admin_obj.append_to_file(admin_obj_df,
                                        new_admin_obj.user_file_path)
#%%
    def register_super_admin(
        self
    )-> bool:
        
        # all variables are validated and follows rules
        #create a customer instance 
        
        user_oper_obj = UserOperation()
        user_name = User.super_admin_uname
        user_password = "superadmin1"
        if not (user_oper_obj.check_username_exist(user_name) and 
                user_oper_obj.validate_user_name(user_name) and 
                user_oper_obj.validate_password(user_password)
                ):
            return False
        else:
            user_id = user_oper_obj.generate_unique_user_id()
            user_register_time = user_oper_obj.return_time_str()
            user_password_encyp = user_oper_obj.encrypt_password(user_password)
            new_admin_obj = Admin(user_id = user_id,
                                  user_name = user_name, 
                                  user_password = user_password_encyp,
                                  user_register_time=user_register_time,
                                  user_role = User.super_admin_role
                                  )
            admin_obj_df = pd.DataFrame(new_admin_obj.__dict__ , index = [0])
            return new_admin_obj.append_to_file(admin_obj_df,
                                        new_admin_obj.user_file_path)
#%%
    def add_new_customer(
        self,
        cust_name: str,
        cust_password: str,
        cust_email: str,
        cust_mobile: str
        ) -> bool : 
        
        return CustomerOperation().register_customer(cust_name, cust_password,
                                              cust_email, cust_mobile)
        
#%%

    def view_customer(
        self,
        search_term: str,
        is_user_id: bool,
        is_page_num: bool
    ) -> tuple : 
        
        if is_user_id : 
            return_df = User().search_return_df(search_term, 
                                                is_user_name = False,
                                                is_user_id= True)
            if return_df.empty : 
                return tuple()
            else: 
                return_df_dict = return_df.to_dict("records")
                return_obj_list = [Customer(**return_df_dict[0])]
                return_tuple = (return_obj_list,0,0)
                return return_tuple
            
        if is_page_num : 
            return_tuple = CustomerOperation().get_customer_list(search_term)
            return return_tuple
#%%

    def delete_customer(
        self,
        is_all_cust: bool,
        is_user_id: bool,
        del_user_id: str
    ) -> bool : 
        """
        deletes all or single customer based on user_id

        Parameters
        ----------
        is_all_cust : bool
            DESCRIPTION.
        is_user_id : bool
            DESCRIPTION.
        del_user_id : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if is_all_cust : 
            return CustomerOperation().delete_all_customers()
        if is_user_id : 
            return CustomerOperation().delete_customer(del_user_id)
#%%

    def delete_admin(
        self,
        is_all_admin: bool,
        is_user_id: bool,
        del_user_id: str
    )-> bool :
        """
        deletes admin and should give all or user id

        Parameters
        ----------
        is_all_admin : bool
            DESCRIPTION.
        is_user_id : bool
            DESCRIPTION.
        del_user_id : str
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if is_user_id :
            curr_user_df = User().search_return_df(del_user_id, is_user_name=False,
                                                   is_user_id=True)
            if curr_user_df.empty : 
                return False
            else : 
                pass
            
            if curr_user_df[User.user_role].isin(
                    [User.customer_role,User.super_admin_role]).bool() :
                return False
            else : 
                pass
            
            user_file_df = User().read_return_df(User.user_file_path)
            del_file_df = user_file_df[
                user_file_df[User.user_id]!= del_user_id].copy()
            return User().write_df_to_file(del_file_df, User.user_file_path)
        
        if is_all_admin : 
            
            user_file_df = User().read_return_df(User.user_file_path)
            del_file_df = user_file_df[ 
                    ~user_file_df[User.user_role].isin([User.admin_role])].copy()
            return User().write_df_to_file(del_file_df, User.user_file_path)
#%%    
            