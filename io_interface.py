import pandas as pd
from model_user import User
"""
This class contains i/o opertaions

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023
"""

#%%
class IOInterface:
    
    line_break = "----------------------------------------------------------------"
    cust_type = "Customer"
    product_type = "Product"
    order_type = "Order"
    
    def get_user_input(
        self, 
        ip_message: str, 
        num_args: int
    ) -> list:
        """
        This method takes input according to specification and returns list of
        inputs

        Parameters
        ----------
        message : str
            DESCRIPTION.
        num_args : int
            DESCRIPTION.

        Returns
        -------
        list
            DESCRIPTION.

        """
        print(ip_message.strip())
        ip_args = input("Please seperate your inputs with whitespace: ").split()
        if len(ip_args) < num_args : 
            ip_args += [""]*(num_args - len(ip_args))
        if len(ip_args) > num_args :
            message = ("Entered too many inputs"
                       f" considering only first {num_args} inputs\n")
            print(message)
            ip_args = ip_args[:num_args]
        return ip_args
    
       
#%%
    def print_error(
        self,
        error_source: str, 
        error_message: str 
    ) -> None:
        """
        Prints error message 

        Parameters
        ----------
        error_source : str
            DESCRIPTION.
        error_message : str
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        # user error source from __qualname__ 
        err_msg = f"Error raised in {error_source}, please check {error_message}"
        print(err_msg+"\n")
#%%

    def print_message(
        self,
        message: str
    ) -> None :
        """
        prints passed string

        Parameters
        ----------
        message : str
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        print(f"{message}")
        
#%%   

    def main_menu(
        self 
    ) -> None :
        """
        main menu function with 3 options to choose from; 

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        self.print_message(self.line_break)
        self.print_message("Welcome to Monash e-store")
        main_menu_message = (f'''\n {self.line_break} \nPlease select an option
                            \n[1]. Login \n[2]. Register \n[3]. Quit
                            \n{self.line_break}''')
        self.print_message(main_menu_message)
        
#%%

    def customer_menu(
        self
    ) -> None: 
        cus_menu_dict = {
            "Options" : ["1","2","3","4","5"],
            "Menu" : ["Profile",
                      "Browse Products",
                      "view order history".title(),
                      "view consumption figures".title(),
                      "Logout"
                      ],
            "Description" : ["view, modify, delete".title(),
                             "browse, search".title(),
                             "view, delete".title(),
                             "order statistics".title(),
                             "Exit"
                             ]
            }
        cus_menu_df = pd.DataFrame(cus_menu_dict)
        self.print_message(cus_menu_df.to_markdown(index = False,
                                                   tablefmt='grid'))
#%%  
    def admin_menu(
        self
    ) -> None:
        admin_menu_dict = {
            "Options" : ["1","2","3","4","5","6"],
            "Menu" : ["Access/ Modify users".title(),
                      "Admin Product Menu",
                      "Admin orders Menu".title(),
                      "View statistics".title(),
                      "Generate test data".title(),
                      "logout".title()
                      ],
            "Description" : ["add, view, delete".title(),
                             "browse, search, load".title(),
                             "delete,browse orders etc..".title(),
                             "analyze trends of produts, orders etc.".title(),
                             "generate test data".title(),
                             "Exit"
                             ]
        }
        admin_menu_df = pd.DataFrame(admin_menu_dict)
        self.print_message(admin_menu_df.to_markdown(index=False,
                                                     tablefmt = "grid"))
#%%
    def customer_profile_options(
        self
    ) -> None :
        customer_profile_message_dict = {
            "Options" : ["1","2","3","4"],
            "Menu" : ["View Profile".title(),
                      "Modify Profile".title(),
                      "Delete Profile".title(),
                      "Go back to previous menu".title()
                     ]
            }
        customer_profile_message_df = pd.DataFrame(
            customer_profile_message_dict)
        self.print_message(customer_profile_message_df.to_markdown(
            index = False, tablefmt = "grid"))
#%%
    def print_object(
        self,
        print_obj
    ) -> None :
        message = print_obj.__str__()
        self.print_message(message)
#%%

    def pretty_print_object(
        self,
        print_obj
    ) -> None :
        """
        beautiful way to print user objects used in view profile

        Parameters
        ----------
        print_obj : TYPE
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        message = ("\nYour profile details are as follows"
                   f"\nUser Name : {print_obj.user_name}"
                   f"\nAccount Active Since : {print_obj.user_register_time}"
                   f"\nEmail Id : {print_obj.user_email}"
                   f"\nMobile : {print_obj.user_mobile}")
        self.print_message(message)
        
#%%

    def show_list(
        self,
        user_role: str,
        list_type: str,
        object_list: list
    ) -> None :
        """
        printts the list of objects pased

        Parameters
        ----------
        user_role : str
            DESCRIPTION.
        list_type : str
            DESCRIPTION.
        object_list : list
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.

        """
        
        permission_message = ("\nCustomers cant view customer list")
        
        if user_role == User.customer_role and list_type == IOInterface.cust_type :
            self.print_message(permission_message)
        else :     
            print_obj = object_list[0]
            page_num = object_list[1]
            total_page = object_list[2]
            
            for obj in print_obj : 
                self.print_message(IOInterface.line_break)
                page_info_message = (f"Page number: {page_num} of total pages"
                                     f" {total_page} ")
                self.print_message(page_info_message)
                self.print_object(obj)
#%%        
        
            