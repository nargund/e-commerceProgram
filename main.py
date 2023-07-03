from operation_customer import CustomerOperation
from operation_admin import AdminOperation
from operation_user import UserOperation
from io_interface import IOInterface
from model_user import User
from model_customer import Customer
from model_admin import Admin
from model_product import Product
from opreation_product import ProductOperation
from operation_order import OrderOperation
import sys
import time

"""
Main class controls entire logic of the program 

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023

"""

#%%
#Global Variables for all operation classes


register = "register"
update = "update"
choose_message = "\nPlease choose from above options"
exit_message = "Returning to main menu\n"
exit_message_prev = "Returning to previous menu\n"
exit_message_prev_check = "\nPress any key to go to previous menu"
exit_message_main_check = "\nPress any key to go to main menu"
customer_menu = "cust_menu"
admin_menu = "admin_menu"
line_break = "\n---------------------------------------------------------------\n"
fail = "\nSomething went wrong"
graph_sucsess = "\nGraphs are saved succesfully"
#%%

def header() -> None:
    
    IOInterface().print_message(IOInterface().line_break)
    message = "Monash e-store"
    IOInterface().print_message(message)
    IOInterface().print_message(IOInterface().line_break)
    
def clear_cls() -> None :
    
    IOInterface().print_message("\033[H\033[J")
    
    
#%%
def user_file_check() -> None:
    temp_user = User()
    
    try: 
        with open(temp_user.user_file_path, temp_user.read_mode) as usr_file : 
            su_check =  AdminOperation().register_super_admin() 
            test_cust = CustomerOperation().register_customer("test_cust", "password123", 
                                                  "sfsf@gmail.com", "0312345678")
            if su_check : 
                message = ('''Super Admin did not exist
                           \nCreated Successfully''')
                IOInterface().print_message(message)
            else:    
                IOInterface().print_message("Super Admin Exists")
    except:
        with open(temp_user.user_file_path,"w+") as usr_file:
            test_cust = CustomerOperation().register_customer("test_cust", "password123", 
                                                  "sfsf@gmail.com", "0312345678")
            su_check = AdminOperation().register_super_admin()
            if su_check : 
                message = ("\nUser file was created successfully" 
                           "\nSuper Admin Created Succesfully")
                IOInterface().print_message(message)
#%%  
def register_user(
    is_cust: bool = True
    ) -> bool:
    
    if is_cust : 
        reg_cust_message = ('''Please enter the below details 
                              \nUser Name, Password, E-mail, Mobile
                              \nPoints to remember while registering:
                              \n* The username should be atleast 5 characters long; I
                              \n\t It should contain only letters or underscore.
                              \n* The password should be atleast 5 characters long;
                              \n\t It should contain atleats one alphabet and one digit.
                              \n* The mobile number should start with 03 0r 04.''')
        
        get_register_ip = IOInterface().get_user_input(reg_cust_message, 4)
        reg_status = CustomerOperation().register_customer(get_register_ip[0],
                                                    get_register_ip[1], 
                                                    get_register_ip[2], 
                                                    get_register_ip[3])
        ret_flag = True
        if not reg_status : 
            error_source = CustomerOperation().register_customer.__qualname__
            error_message = ("Please check if you are adhering to rules"
                             "\nIf yes! retry with other username according"
                             " to rules")
            IOInterface().print_error(error_source, error_message)
            ip_message = "To retry click [X]"
            
            retry_ip = IOInterface().get_user_input(ip_message, 1)
            if retry_ip[0].lower() == "x" :
                register_user()
            else : 
                reg_status =  True
                ret_flag = False
        else: ret_flag = True
        return ret_flag
    
    if not is_cust:
        #super admin status already checked 
        reg_admin_message = ('''Hello super admin
                          \nPlease enter Username and Password for new admin''')
        
        get_register_ip = IOInterface().get_user_input(reg_admin_message, 2)
        su_message = ("Is new admin super admin? [Y] for yes")
        
        is_super_admin_ip = IOInterface().get_user_input(su_message, 1)
        if is_super_admin_ip[0].lower() == 'y' :
            IOInterface().print_message("Creating Super Admin")
            is_super_admin = True
        else: 
            IOInterface().print_message("Creating Admin")
            is_super_admin = False   
            
        reg_status = AdminOperation().register_customer(get_register_ip[0],
                                                    get_register_ip[1], 
                                                    is_super_admin)
        ret_flag = True
        if not reg_status : 
            error_source = AdminOperation().register_customer.__qualname__
            error_message = "Registration Unsuccessful!"
            IOInterface().print_error(error_source, error_message)
            ip_message = "To retry click [X]"
            
            retry_ip = IOInterface().get_user_input(ip_message, 1)
            if retry_ip[0].lower() == "x" :
                register_user(is_cust = False)
            else : 
                reg_status =  True
                ret_flag = False
        else: ret_flag = True
        return ret_flag
#%%  
def customer_profile_control(
    oper_type: str
) -> None :
    
    
    if oper_type == register : 
        if register_user() :
            message = ("Register Succesful") 
            IOInterface().print_message(message)
            IOInterface().print_message("Returning to main menu\n")
            time.sleep(2)
            return run_main() 
        else:
            reg_fail_message = "Registration failed going back to main menu\n"
            IOInterface().print_message(reg_fail_message)
            IOInterface().print_message("Returning to main menu\n")
            time.sleep(2)
            return run_main()
#%%            
def attempt_login(
    user_name,
    user_password    
) : 
    login_succ = UserOperation().login(user_name, user_password)
    if login_succ.user_name == User.default_user_name :
        return False
    
    if login_succ.user_role == User.customer_role :
        return True
    if login_succ.user_role in (User.super_admin_role, User.admin_role) :
        return True
    

def login_control():
    
    clear_cls()
    header()
    login_ip_message = "Hello user!, please enter User Name and Password:"
    wrong_creds_message = ("Credentials are wrong or improper input\n"
                           "Press [Z] to retry, any other key "
                            "to go back to previous menu")
    login_control_size = 2
    
    login_details = IOInterface().get_user_input(login_ip_message, 
                                             login_control_size)
    
    login_status = attempt_login(login_details[0], login_details[1])
    
    if not login_status :
        creds_ip = IOInterface().get_user_input(wrong_creds_message, 1)
        if creds_ip[0].lower() == "z" :
            #del login_details, login_status, creds_ip
            return login_control()
        else :
            IOInterface().print_message(line_break + exit_message)
            time.sleep(3)
            return run_main()
            
    else :          
        user_obj = UserOperation().login(login_details[0], login_details[1])   
        if user_obj.user_role == User.customer_role :
            return run_customer_menu(user_obj)
            
        if user_obj.user_role in (User.super_admin_role, User.admin_role) :
            return run_admin_menu(user_obj)
#%%
def run_customer_menu(
    cust_obj: Customer
):
    
    clear_cls()
    header()
    cust_greet_message = (f"Hello {cust_obj.user_name}!\n"
                          "Your menu options are\n")
    IOInterface().print_message(cust_greet_message)
    cust_menu_ip_message = choose_message
    cust_menu_true_list = ["1","2","3","4","5"]
    cust_menu_ip_size = 1
    valid_message = (f"Please re-enter from {cust_menu_true_list}"
                    " or choose [5] to exit")
    IOInterface().customer_menu()
    cust_menu_ip = ""
    while True : 
        cust_menu_ip = IOInterface().get_user_input(cust_menu_ip_message, 
                                                cust_menu_ip_size)
        if any ( ip not in cust_menu_true_list for ip in cust_menu_ip)  : 
            IOInterface().print_message(valid_message)
            continue
        else: break
            
    if cust_menu_ip[0] == "1" :
        return customer_profile_options(cust_obj)
    elif cust_menu_ip[0] == "2" :
        return customer_browse_products(cust_obj)
    elif cust_menu_ip[0] == "3" :
        return customer_order_options(cust_obj)
    elif cust_menu_ip[0] == "4" :
        return customer_consumption_options(cust_obj)
    elif cust_menu_ip[0] == "5" :
        return run_main()
#%%
def run_admin_menu(
    admin_obj: Admin
)-> None:
    
    clear_cls()
    header()
    admin_greet_message = (f"Hello {admin_obj.user_name}\n"
                           "Your menu options are:")
    IOInterface().print_message(admin_greet_message)
    admin_menu_ip_message = choose_message
    admin_menu_true_list = ["1","2","3","4","5","6"]
    admin_menu_ip_size = 1
    valid_message = "Hint: Please re-enter or choose [6] to exit"
    IOInterface().admin_menu()
    
    admin_menu_ip = ""
    while True : 
        admin_menu_ip = IOInterface().get_user_input(admin_menu_ip_message, 
                                                admin_menu_ip_size)
        if any ( ip not in admin_menu_true_list for ip in admin_menu_ip)  : 
            IOInterface().print_message(valid_message)
            continue
        else: break            
    if admin_menu_ip[0] == "1" :
        return admin_profile_options(admin_obj)
    elif admin_menu_ip[0] == "2" :
        return admin_product_options(admin_obj)
    elif admin_menu_ip[0] == "3" :
        return admin_order_options(admin_obj)
    elif admin_menu_ip[0] == "4" :
        return admin_consumption_options(admin_obj)
    elif admin_menu_ip[0] == "5" :
        return admin_generate_test_data(admin_obj)
    elif admin_menu_ip[0] == "6" :
        return run_main()
#%% Cust Menu Working 
def customer_profile_options(
        cust_obj
    ):
    
    
    clear_cls()
    header()
    cust_profile_option_message = ("[1] : View Account\n"
                                   "[2] : Modify Account\n"
                                   "[3] : Delete Account\n"
                                   "[4] : Return to Previous Menu\n"
                                   )
    cust_profile_true_list = ["1","2","3","4"]
    cust_profile_valid_message = (f"Hint: Please re-enter from {cust_profile_true_list}"
                                  " or choose [4] to return"
                                  " to previous menu")
    
    modify_user_true_list = ["1","2","3","4"]
    modify_list_attr = [User.user_password,User.user_email,User.user_mobile
                         ,"Exit"]
    attribute_dict = dict(zip(modify_user_true_list,modify_list_attr))
    modify_user_message = ("\n\nPlease choose attribute to modify from below\n"
                           "[1] : Password\n"
                           "[2] : Email Id\n"
                           "[3] : Mobile\n"
                           "[4] : Cancel\n")
    modify_list_valid_message = ("Hint: Please re-enter from"
                                 f"{modify_user_true_list}"
                                 "or choose [4] to return to previous menu")
    modify_attribute_ip_size = 1
    cust_profile_ip_size = 1
    IOInterface().print_message(cust_profile_option_message)
    delete_profile_warning = ("Please note your order history may not be "
                              "deleted from our database \nRest assured "
                              "your profile is deleted")
    
    cust_profile_ip = ""
    while True : 
        cust_profile_ip = IOInterface().get_user_input(choose_message, 
                                                cust_profile_ip_size)
        if any ( _ not in cust_profile_true_list for _ in cust_profile_ip)  : 
            IOInterface().print_message(cust_profile_valid_message)
            continue
        else: 
            break
    
    if cust_profile_ip[0] == "1" :
        IOInterface().pretty_print_object(cust_obj)
        exit_ip = IOInterface().get_user_input(
            line_break + exit_message_prev_check, 1)
        if len(exit_ip) != 0 :
            IOInterface().print_message(exit_message_prev)
            return customer_profile_options(cust_obj)
        else: 
            IOInterface().print_message(exit_message_prev)
            return customer_profile_options(cust_obj)
    if cust_profile_ip[0] == "2" :
        IOInterface().pretty_print_object(cust_obj)
        IOInterface().print_message(modify_user_message)
        while True : 
            modify_attribute = IOInterface().get_user_input(choose_message, 
                                                    modify_attribute_ip_size)
            if any ( _ not in modify_user_true_list for _ in modify_attribute): 
                IOInterface().print_message(modify_list_valid_message)
                continue
            else: 
                break  
        if modify_attribute[0] == "1" :
            value = IOInterface().get_user_input("Enter new password", 1)
        elif modify_attribute[0] == "2" :
            value = IOInterface().get_user_input("Enter new Email Id", 1)
        elif modify_attribute[0] == "3" :
            value = IOInterface().get_user_input("Enter new Mobile", 1)
        elif modify_attribute[0] == "4" :
            return customer_profile_options(cust_obj)
        
        update_status = CustomerOperation().update_customer(
            attribute_dict[modify_attribute[0]], value[0], cust_obj)
        if update_status :
            IOInterface().print_message("Update Succesful")
            IOInterface().print_message(("\nNote: Changes may take some time "
                                        "to reflect"))
            _ = IOInterface().get_user_input(
                line_break+exit_message_prev_check, 1)
            return customer_profile_options(cust_obj)
        else :
            IOInterface().print_message("Update Unsuccesful")
            _ = IOInterface().get_user_input(
                line_break+exit_message_prev_check, 1)
            return customer_profile_options(cust_obj)
    if cust_profile_ip[0] == "3" :
        confirm_ip = IOInterface().get_user_input("Press [X] key to confirm", 1)
        if confirm_ip[0].lower() == "x" : 
            del_flag = CustomerOperation().delete_customer(cust_obj.user_id)
        else : 
            IOInterface().print_message(line_break + exit_message_prev)
            time.sleep(2)
            return customer_profile_options(cust_obj)
        if del_flag : 
            IOInterface().print_message("Profile deleted succesfully")
            IOInterface().print_message(delete_profile_warning)
            _ = IOInterface().get_user_input(exit_message_main_check, 1)
            return run_main()
        else : 
            IOInterface().print_message("Profile deleted unsuccesful"
                                        " Something went wrong")
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return customer_profile_options(cust_obj)
    if cust_profile_ip[0] == "4" :
        IOInterface().print_message(exit_message_prev)
        time.sleep(2)
        return run_customer_menu(cust_obj)
#%% 
def cust_browse_page(
    cust_obj,
    page_number:str
    ):
    
    browse_message = ("**The products are**\n")
    order_message = (f"{line_break}\n[1] : To order from above\n"
                     "[2] : To browse other page\n"
                     f"[3] : To go back to previous menu\n{line_break}")
    
    browse_page_true_list = ["1","2","3"]
    browse_page_valid_message = ("Hint: Please re-enter or choose [3] to return"
                                  " to previous menu")
    order_successful_message = "Order pleaced successfully\n"
    order_unsuccessful_message = "Oops! something went wrong! please try again\n"
    browse_page_option_size = 1
    if page_number in ("", None): 
        page_number = "0"
    products_tuple = ProductOperation().get_product_list(page_number)
    disp_products = list(products_tuple)
    page_num_invalid_message = ("Invalid page number please choose from 1"
                                f" to {disp_products[2]}")
    
    if len(disp_products[0]) == 0  :
        IOInterface().print_message(page_num_invalid_message)
        err_page = IOInterface().get_user_input("Enter valid page number or [X] to exit", 1)
        if err_page[0].lower() == "x" :
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return customer_browse_products(cust_obj)
        else : 
            return cust_browse_page(cust_obj, err_page[0])
    
    IOInterface().print_message(browse_message)    
    IOInterface().show_list(cust_obj.user_role, IOInterface.product_type, 
                             disp_products)   
    
    browse_page_ip = ""
    while True : 
        browse_page_ip = IOInterface().get_user_input(order_message, 
                                                browse_page_option_size)
        if any ( _ not in browse_page_true_list for _ in browse_page_ip)  : 
            IOInterface().print_message(browse_page_valid_message)
            continue
        else: 
            break
    
    if browse_page_ip[0] == "1" :
        product_id = IOInterface().get_user_input("Enter Product ID: ", 1)
        order_flag = OrderOperation().create_an_order(
            customer_id = cust_obj.user_id, 
            product_id = product_id[0])
        if order_flag :
            IOInterface().print_message(order_successful_message)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return customer_browse_products(cust_obj)
        else : 
            IOInterface().print_message(order_unsuccessful_message)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return cust_browse_page(cust_obj, page_number)     
    
    if browse_page_ip[0] == "2" :
        new_page = IOInterface().get_user_input("Enter page", 1)
        return cust_browse_page(cust_obj, new_page[0])
        
    if browse_page_ip[0] == "3" :
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
        return customer_browse_products(cust_obj)
#%%   
def cust_search_page(cust_obj) : 
    clear_cls()
    header()
    search_page_message = ("[1] : Search by product Id\n"
                           "[2] : Search by product name\n"
                           "[3] : Return to previous menu\n"
                           "Please note if you choose [1] and [2] enter "
                           "search term with whitespace (eg: 2 bronze)")
    
    order_message = (f"{line_break}\n[1] : To order from above\n"
                     "[2] : To search other product\n"
                     "[3] : To go back to previous menu\n")
    
    search_page_true_list = ["1","2","3"]
    search_page_valid_message = ("Hint: Please re-enter or choose [3] to return"
                                  " to previous menu")
    order_successful_message = "Order placed successfully\n"
    order_unsuccessful_message = "Oops! something went wrong! please try again\n"
    search_page_option_size = 2 
    IOInterface().print_message(search_page_message)
    
    search_page_ip = ""
    while True : 
        search_page_ip = IOInterface().get_user_input(choose_message, 
                                                search_page_option_size)
        if len(search_page_ip)>=2 and search_page_ip[0] in search_page_true_list  : 
            break
        else:
            IOInterface().print_message(search_page_valid_message)
            continue   
        
    if search_page_ip[0] == "1" :
        product_id = search_page_ip[1] 
        disp_prod_tuple = ProductOperation().get_product_by_id(
            search_page_ip[1])
        disp_prod_list = list(disp_prod_tuple)
        
        if len(disp_prod_list[0]) == 0 : 
            _ = IOInterface().get_user_input(("\nSomething went wrong\n"+
                                              line_break+exit_message_prev_check),
                                             1)
            cust_search_page(cust_obj)
        IOInterface().show_list(cust_obj.customer_role, IOInterface.product_type,
                                disp_prod_list)
        while True : 
            order_ip = IOInterface().get_user_input(order_message, 
                                                    1)
            if any ( _ not in search_page_true_list for _ in order_ip) : 
                IOInterface().print_message(search_page_valid_message)
                continue
            else: 
                break
        
        if order_ip[0] == "1" :
            #need to take product_id input, product_id already taken
            IOInterface().print_message("Confirming your order!\n")
            product_id = search_page_ip[1]
            order_flag = OrderOperation().create_an_order(
                customer_id = cust_obj.user_id, 
                product_id = product_id)
            if order_flag :
                IOInterface().print_message(order_successful_message)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
                return customer_browse_products(cust_obj)
            else : 
                IOInterface().print_message(order_unsuccessful_message)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
                return cust_search_page(cust_obj)
        
        if order_ip[0] == "2" :
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return cust_search_page(cust_obj)
            
        if order_ip[0] == "3" :
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return cust_search_page(cust_obj)
                
    if search_page_ip[0] == "2" : 
        
        keyword = search_page_ip[1]
        disp_prod_tuple = ProductOperation().get_product_list_by_keyword(keyword)
        disp_prod_list = list(disp_prod_tuple)
        
        if len(disp_prod_list[0]) == 0 : 
            _ = IOInterface().get_user_input("\nSomething went wrong\n"+exit_message_prev_check,
                                             1)
            return cust_search_page(cust_obj)
            
        IOInterface().show_list(cust_obj.customer_role, IOInterface.product_type,
                                disp_prod_list)    
        order_ip = ""
        while True : 
            order_ip = IOInterface().get_user_input(order_message, 
                                                    1)
            if any ( _ not in search_page_true_list for _ in order_ip) : 
                IOInterface().print_message(search_page_valid_message)
                continue
            else: 
                break
        if order_ip[0] == "1" :
            #need to take product_id input, product_id already taken
            product_id_list = IOInterface().get_user_input("Enter product Id", 
                                                           1)
            product_id = product_id_list[0]
            order_flag = OrderOperation().create_an_order(
                customer_id = cust_obj.user_id, 
                product_id = product_id)
            if order_flag :
                IOInterface().print_message(order_successful_message)
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return customer_browse_products(cust_obj)
            else : 
                IOInterface().print_message(order_unsuccessful_message)
                return cust_search_page(cust_obj)
        if order_ip[0] == "2" :
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return cust_search_page(cust_obj)
            
        if order_ip[0] == "3" :
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return cust_search_page(cust_obj)
    if search_page_ip[0] == "3" : 
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
        return customer_browse_products(cust_obj)
        
#%%
def customer_browse_products(cust_obj) -> None :
    
    clear_cls()
    header()
    cust_browse_option_message = ("[1] : Browse Products\n"
                                   "[2] : Search Products\n"
                                   "[3] : Return to Previous Menu\n"
                                   )
    cust_browse_true_list = ["1","2","3"]
    cust_browse_valid_message = ("Hint: Please re-enter or choose [3] to return"
                                  " to previous menu")
    page_number_message = ("Page number not entered please enter!")
    cust_browse_option_size = 2    
    IOInterface().print_message(cust_browse_option_message)
    
    cust_browse_ip = ""
    while True : 
        cust_browse_ip = IOInterface().get_user_input(choose_message, 
                                                cust_browse_option_size)
        if len(cust_browse_ip)>=2 and cust_browse_ip[0] in cust_browse_true_list  : 
            break
        else:
            IOInterface().print_message(cust_browse_valid_message)
            continue    
    
    if cust_browse_ip[0] == "1" :
        
        if len(cust_browse_ip[1]) == 0 :
            page_number = IOInterface().get_user_input(page_number_message,1)
        else: 
            page_number = [cust_browse_ip[1]]
        return cust_browse_page(cust_obj,page_number[0])
    
    if cust_browse_ip[0] == "2" :
        return cust_search_page(cust_obj)
        
    if cust_browse_ip[0] == "3" :
        IOInterface().print_message(line_break+exit_message_prev)
        time.sleep(2)
        return run_customer_menu(cust_obj)
        
#%%
def customer_order_options(cust_obj) -> None :
    clear_cls()
    header()
    cust_order_option_message = ("[1] : View your Orders\n"
                                   "[2] : Cancel Order\n"
                                   "[3] : Return to Previous Menu\n"
                                   )
    cust_order_true_list = ["1","2","3"]
    cust_order_valid_message = ("Hint: Please re-enter or choose [3] to return"
                                  " to previous menu")
    cust_order_option_size = 1
    no_orders_message = (f"{line_break}Oh Oh! Dont have any orders yet"
                         "\ngo ahead and order few")
    delete_order_message = (f"{line_break} Please enter order Id if unsure "
                            "use view order option")
    
    IOInterface().print_message(cust_order_option_message)
    
    cust_order_ip = ""
    while True : 
        cust_order_ip = IOInterface().get_user_input(choose_message, 
                                                cust_order_option_size)
        if any ( _ not in cust_order_true_list for _ in cust_order_ip)  : 
            IOInterface().print_message(cust_order_valid_message)
            continue
        else: 
            break
    
    if cust_order_ip[0] == "1" : 
        
        page_num = IOInterface().get_user_input("Enter Page Number", 1)
        order_disp_tuple = OrderOperation().get_order_list(
            customer_id = cust_obj.user_id, 
            page_number = page_num[0])
        order_disp_list = list(order_disp_tuple)
        page_num_invalid_message = ("Invalid page number please choose from 1"
                                    f" to {order_disp_list[2]}")
        
        
        if order_disp_list[2] == "0" : 
           IOInterface().print_message(no_orders_message)
           _ = IOInterface().get_user_input(line_break+exit_message_main_check, 1)
           return run_customer_menu(cust_obj)
        
        if len(order_disp_list[0]) == 0 :
            IOInterface().print_message(page_num_invalid_message)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return customer_order_options(cust_obj)
        
        IOInterface().show_list(user_role = cust_obj.user_role, 
                                list_type = IOInterface.order_type, 
                                object_list = order_disp_list)
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
        return customer_order_options(cust_obj)
    
    if cust_order_ip[0] == "2" :
        order_id_list = IOInterface().get_user_input(delete_order_message, 1)
        del_flag = OrderOperation().delete_order(order_id_list[0])
        if del_flag : 
            IOInterface().print_message("\nOrder deleted succesfully")
            _ = IOInterface().get_user_input(line_break+exit_message_main_check, 1)
            return run_customer_menu(cust_obj)
        else : 
            IOInterface().print_message("\nOrder deleted unsuccesfully")
            _ = IOInterface().get_user_input(line_break+exit_message_main_check, 1)
            return run_customer_menu(cust_obj)
    if cust_order_ip[0] == "3" :
        _ = IOInterface().get_user_input(line_break+exit_message_main_check, 1)
        return run_customer_menu(cust_obj)
        
         

def customer_consumption_options(cust_obj) -> None :
    clear_cls()
    header()
    cust_consumption_option_message = ("[1] : Generate Order Statistics\n"
                                       "[2] : Return to Previous Menu\n"
                                   )
    cust_consumption_true_list = ["1","2"]
    cust_consumption_valid_message = ("Hint: Please re-enter or choose [2] to return"
                                  " to previous menu")
    cust_consumption_option_size = 1 
    IOInterface().print_message(cust_consumption_option_message)
    
    cust_consumption_ip = ""
    while True : 
        cust_consumption_ip = IOInterface().get_user_input(choose_message, 
                                                cust_consumption_option_size)
        if any ( _ not in cust_consumption_true_list for _ in cust_consumption_ip)  : 
            IOInterface().print_message(cust_consumption_valid_message)
            continue
        else: 
            break      
        
    if cust_consumption_ip[0] == "1" :
        if(OrderOperation().generate_single_customer_consumption_figure(
                cust_obj.user_id)) : 
            IOInterface().print_message("\nGraphs are saved succesfully")
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 
                                             1)
            return run_customer_menu(cust_obj)
        else : 
            IOInterface().print_message("\nSomething went wrong!")
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 
                                             1)
            return run_customer_menu(cust_obj)
            
    if cust_consumption_ip[0] == "2" : 
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 
                                         1)
        return run_customer_menu(cust_obj)
#%% admin view 
def admin_view_control(
    admin_obj,
    operation
    )  : 
    view_message = ("[1] : View customer by user_id\n"
                    "[2] : View customer list by page numbers\n"
                    "[3] : Return to Previous Menu")
    view_true_list = ["1","2","3"]
    view_valid = "Wrong input re-enter or [3] to return to Previous Menu"
    
    view_ip = ""
    if operation == "1" :
        while True : 
            view_ip = IOInterface().get_user_input(view_message, 
                                                    1)
            if any ( _ not in view_true_list for _ in view_ip)  :    
                IOInterface().print_message(view_valid)
                continue
            else: 
                break
        if view_ip[0] == "1" :     
            search_term = IOInterface().get_user_input("Enter User Id", 1)
            disp_tuple = AdminOperation().view_customer(
                search_term = search_term[0], is_user_id = True, is_page_num = False) 
            if len(disp_tuple) == 0 :
                IOInterface().print_message("Wrong user Id")
                IOInterface().print_message(line_break+exit_message_prev)
                time.sleep(2)
                return admin_view_control(admin_obj, "1")
            else : 
                disp_list = list(disp_tuple)
                IOInterface().show_list(User.admin_role, IOInterface.cust_type,
                                        disp_list)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
                return admin_view_control(admin_obj, "1")
        if view_ip[0] == "2" : 
            search_term = IOInterface().get_user_input("Enter page number",
                                                       1)
            disp_tuple = AdminOperation().view_customer(search_term = search_term[0], 
                                                        is_user_id = False, 
                                                        is_page_num = True)
            disp_list = list(disp_tuple)
            check_list = disp_list[0]
            if len(check_list) == 0 :
                IOInterface().print_message("Wrong Page Number")
                IOInterface().print_message(line_break+exit_message_prev)
                time.sleep(2)
                return admin_view_control(admin_obj, "1")
            else : 
                disp_list = list(disp_tuple)
                IOInterface().show_list(User.admin_role, IOInterface.cust_type,
                                        disp_list)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
                return admin_view_control(admin_obj, "1")
        if view_ip[0] == "3" : 
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_profile_options(admin_obj)
#%% admin opertations     

def admin_delete_control(admin_obj) -> None :
    delete_message = (f"{line_break}[1] : Delete Customer\n"
                      "[2] : Delete Admins (only super admins)\n"
                      "[3] : Return to Previous Menu\n")
    
    delete_true_list = ["1","2","3"]
    delete_valid = "Wrong input re-enter or [3] to return to Previous Menu"
    delete_cust_message = (f"{line_break}[1]: Delete by user id\n"
                           "[2]: Delete all customers")
    
    delete_admin_message = (f"{line_break}[1]: Delete by user id\n"
                           "[2]: Delete all admins")
    delete_profile_warning = ("Please note customer order history may not be "
                              "deleted from our database \nRest assured "
                              "customer profile is deleted")
    
    delete_ip = ""
    while True : 
        delete_ip = IOInterface().get_user_input(delete_message, 
                                                1)
        if any ( _ not in delete_true_list for _ in delete_ip)  :    
            IOInterface().print_message(delete_valid)
            continue
        else: 
            break
        
    if delete_ip[0] == "1" : 
        option_ip = IOInterface().get_user_input(delete_cust_message, 1)
        if option_ip[0] not in ("1","2") : 
            IOInterface().print_message("\nWrong Option Entered")
            IOInterface().print_message(exit_message_prev)
            time.sleep(2)
            return admin_delete_control(admin_obj)
        elif option_ip[0] == "1" :
            del_user_id = IOInterface().get_user_input("Enter User_ID", 1)
            del_flag = CustomerOperation().delete_customer(del_user_id[0])
            if del_flag : 
                IOInterface().print_message("Customer deleted succesfully")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                IOInterface().print_message(delete_profile_warning)
                return admin_delete_control(admin_obj)
            else : 
                IOInterface().print_message("Customer delete unsuccesful"
                                            " Something went wrong")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
        elif option_ip[0] == "2" : 
            confirm_ip = IOInterface().get_user_input("Press [X] key to confirm", 1)
            if confirm_ip[0].lower() == "x" : 
                del_flag = CustomerOperation().delete_all_customers()
            else : 
                IOInterface().print_message(exit_message_prev)
                time.sleep(2)
                return admin_delete_control(admin_obj)
            if del_flag : 
                IOInterface().print_message("Customers deleted succesfully")
                IOInterface().print_message(delete_profile_warning)
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
            else : 
                IOInterface().print_message("Customers deleted unsuccesful"
                                            " Something went wrong")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
                
    if delete_ip[0] == "2" : 
        if admin_obj.user_role != User.super_admin_role : 
            IOInterface().print_message("\n You are unauthorized")
            IOInterface().print_message(exit_message_prev)
            time.sleep(2)
            return admin_delete_control(admin_obj)
        option_ip = IOInterface().get_user_input(delete_admin_message, 1)
        if option_ip[0] not in ("1","2") : 
            IOInterface().print_message("\nWrong Option Entered")
            IOInterface().print_message(exit_message_prev)
            time.sleep(2)
            return admin_delete_control(admin_obj)
        elif option_ip[0] == "1" :
            del_user_id = IOInterface().get_user_input("Enter User_ID", 1)
            del_flag = AdminOperation().delete_admin(is_all_admin = False, 
                                                     is_user_id = True, 
                                                     del_user_id=del_user_id[0])
            if del_flag : 
                IOInterface().print_message("Admin deleted succesfully")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
            else : 
                IOInterface().print_message("Admin delete unsuccesful"
                                            " Something went wrong")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
        elif option_ip[0] == "2" : 
            confirm_ip = IOInterface().get_user_input("Press [X] key to confirm", 1)
            if confirm_ip[0].lower() == "x" : 
                del_flag = AdminOperation().delete_admin(is_all_admin = True, 
                                                         is_user_id = False, 
                                                         del_user_id="")
            else : 
                IOInterface().print_message(exit_message_prev)
                time.sleep(2)
                return admin_delete_control(admin_obj)
            if del_flag : 
                IOInterface().print_message("Admins deleted succesfully")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
            else : 
                IOInterface().print_message("Admins deleted unsuccesful"
                                            " Something went wrong")
                _ = IOInterface().get_user_input(exit_message_prev_check, 1)
                return admin_delete_control(admin_obj)
                
    if delete_ip[0] == "3" : 
        IOInterface().print_message(exit_message_prev)
        time.sleep(2)
        return admin_profile_options(admin_obj)
        
    
#%%       
def admin_add_control(admin_obj) -> None : 
    add_message = (f"{line_break}[1] : Add Customer\n"
                   "[2] : Add Admins and Super Admins (only super admins)\n"
                   "[3] : Return to Previous Menu\n")
    
    cust_add_message = (f"{line_break}Enter UserId, Password, Email and Mobile of "
                        "new customer"
                        "\nPlease follow the rules of customer profile"
                        "\nNote: every whitespace seperates inputs")
    
    admin_add_message = (f"{line_break}Enter UserId, Password of "
                        "new admin"
                        "\nPlease follow the rules of admin profile"
                        "\nNote: every whitespace seperates inputs")
    add_true_list = ["1","2","3"]
    add_valid = "Wrong input re-enter or [3] to return to Previous Menu"
    
    add_ip =""
    while True : 
        add_ip = IOInterface().get_user_input(add_message, 
                                                1)
        if any ( _ not in add_true_list for _ in add_ip)  :    
            IOInterface().print_message(add_valid)
            continue
        else: 
            break
    
    if add_ip[0] == "1" : 
        new_cust = IOInterface().get_user_input(cust_add_message, 4)
        add_flag = AdminOperation().add_new_customer(cust_name = new_cust[0], 
                                                     cust_password = new_cust[1], 
                                                     cust_email = new_cust[2], 
                                                     cust_mobile = new_cust[3]
                                                     )
        if add_flag : 
            IOInterface().print_message(f"{line_break}New Customer added succesfully")
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return admin_add_control(admin_obj)
        else : 
            IOInterface().print_message(f"{line_break}New Customer add unsuccesful"
                                        " something went wrong")
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return admin_add_control(admin_obj)
            
    if add_ip[0] == "2" : 
        if admin_obj.user_role != User.super_admin_role : 
            IOInterface().print_message("\n You are unauthorized")
            IOInterface().print_message(exit_message_prev)
            time.sleep(2)
            return admin_add_control(admin_obj)
            
        new_admin = IOInterface().get_user_input(admin_add_message, 2)
        super_admin = IOInterface().get_user_input("\nPress [X] if super admin", 
                                                      1)
        if super_admin[0].lower() == "x" : 
            IOInterface().print_message("Creating super admin\n")
            is_super_admin = True
        else : 
            IOInterface().print_message("Creating non super admin\n")
            is_super_admin = False
            
        add_flag = AdminOperation().register_admin(new_admin[0], new_admin[1],
                                                   is_super_admin)
        if add_flag : 
            IOInterface().print_message(f"{line_break}New Admin added succesfully")
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return admin_add_control(admin_obj)
        else : 
            IOInterface().print_message(f"{line_break}New Admin add unsuccesful"
                                        " something went wrong")
            _ = IOInterface().get_user_input(exit_message_prev_check, 1)
            return admin_add_control(admin_obj)
        
    if add_ip[0] == "3" : 
        IOInterface().print_message(exit_message_prev)
        time.sleep(2)
        return admin_profile_options(admin_obj)

#%%         
def admin_profile_options(admin_obj) -> None :
    
    clear_cls()
    header()
    admin_profile_option_message = ("[1] : View Customers\n"
                                   "[2] : Delete Customer and Admin\n"
                                   "[3] : Add Admins and Customers\n"
                                   "[4] : Return to Previous Menu\n"
                                   )
    admin_profile_true_list = ["1","2","3","4"]
    admin_profile_valid_message = ("Hint: Please re-enter or choose [4] to return"
                                  " to previous menu")
    admin_profile_ip_size = 1
    IOInterface().print_message(admin_profile_option_message)
    
    admin_profile_ip = ""
    while True : 
        admin_profile_ip = IOInterface().get_user_input(choose_message, 
                                                admin_profile_ip_size)
        if any ( _ not in admin_profile_true_list for _ in admin_profile_ip)  :    
            IOInterface().print_message(admin_profile_valid_message)
            continue
        else: 
            break
    if admin_profile_ip[0] == "1" :
        return admin_view_control(admin_obj,"1")
    if admin_profile_ip[0] == "2" : 
        return admin_delete_control(admin_obj)
    if admin_profile_ip[0] == "3" : 
        return admin_add_control(admin_obj)    
    if admin_profile_ip[0] == "4" : 
        return run_admin_menu(admin_obj)
#%%    
def admin_browse_page(admin_obj,page_number) : 
    if page_number in ("", None): 
        page_number = "0"
    admin_browse_message = "\n*The Products are*\n"
    disp_prod_tuple = ProductOperation().get_product_list(page_number)
    disp_prod_list = list(disp_prod_tuple)
    page_num_invalid_message = ("Invalid page number please choose from 1"
                                f" to {disp_prod_list[2]}")
    
    if len(disp_prod_list[0]) == 0  :
        IOInterface().print_message(page_num_invalid_message)
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
        return admin_product_options(admin_obj) 
        
    IOInterface().print_message(admin_browse_message)
    IOInterface().show_list(admin_obj.user_role, IOInterface.product_type, 
                             disp_prod_list)
    _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
    return admin_product_options(admin_obj)
    
def admin_search_page(admin_obj,product_id) : 
    
    admin_browse_message = "\n*The Product details are*\n"
    disp_prod_tuple = ProductOperation().get_product_by_id(
        product_id)
    disp_prod_list = list(disp_prod_tuple)
    
    if len(disp_prod_list[0]) == 0 : 
        _ = IOInterface().get_user_input(("{line_break}\nSomething went wrong\n"
                                         +line_break+exit_message_prev_check),
                                         1)
        return admin_product_options(admin_obj)
        
    IOInterface().print_message(admin_browse_message)
    IOInterface().show_list(admin_obj.user_role, IOInterface.product_type, 
                             disp_prod_list)
    _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
    return admin_product_options(admin_obj)

#%%
def admin_product_options(admin_obj) -> None :
    
    
    clear_cls()
    header()
    admin_product_option_message = (f"{line_break}\n[1] : Load Products\n"
                                    "[2] : Browse Products\n"
                                    "[3] : Search Product by ID\n"
                                   "[4] : Delete Product by product Id\n"
                                   "[5] : Delete all Products\n" 
                                   "[6] : Return to Previous Menu\n"
                                   )
    admin_product_true_list = ["1","2","3","4","5","6"]
    admin_product_valid_message = ("Wrong Input \n"
                                   "Hint: Please re-enter or choose [6] to return"
                                  " to previous menu")
    
    admmin_product_del_success = "\nProduct deleted succesfully"
    admmin_product_del_fail = "\nSomething went wrong! Couldnt delete"
    admin_product_option_size = 1  
    IOInterface().print_message(admin_product_option_message)
    
    admin_product_ip = ""
    while True : 
        admin_product_ip = IOInterface().get_user_input(choose_message, 
                                                admin_product_option_size)
        if any ( _ not in admin_product_true_list for _ in admin_product_ip)  :    
            IOInterface().print_message(admin_product_valid_message)
            continue
        else: 
            break
        
    if admin_product_ip[0] == "1" : 
        confirm_ip = IOInterface().get_user_input(("\n[X] to confirm "
                                                  "load may overwrite"), 
                                                  1)
        if confirm_ip[0].lower() == "x" : 
            ProductOperation().extract_products_from_files()
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)
        else : 
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)
            
    if admin_product_ip[0] == "2" : 
        page_num_list = IOInterface().get_user_input(
            "\nPlease enter page number: ", 1)
        page_number = page_num_list[0]
        return admin_browse_page(admin_obj,page_number)
    
    if admin_product_ip[0] == "3" : 
        page_num_list = IOInterface().get_user_input(
            "\nPlease enter Product ID: ", 1)
        product_id = page_num_list[0]
        return admin_search_page(admin_obj,product_id)
    
    if admin_product_ip[0] == "4" : 
        del_prod_list = IOInterface().get_user_input("\nEnter Product Id :", 
                                                     1)
        del_flag = ProductOperation().delete_product(del_prod_list[0])
        if del_flag :
            IOInterface().print_message(admmin_product_del_success)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)
        else : 
            IOInterface().print_message(admmin_product_del_fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)

    if admin_product_ip[0] == "5" : 
        confirm_ip = IOInterface().get_user_input(("\n[X] to confirm "
                                                  "delete all products!"), 
                                                  1)
        if confirm_ip[0].lower() == "x" : 
            ProductOperation().delete_all_products()
            IOInterface().print_message(admmin_product_del_success)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)
        else : 
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_product_options(admin_obj)    
            
    if admin_product_ip[0] == "6" :
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
        return run_admin_menu(admin_obj)
#%%
def admin_order_options(admin_obj) -> None :
    
    
    clear_cls()
    header()
    admin_order_option_message = ("[1] : Cancel Order by Order ID\n"
                                   "[2] : Delete all Orders\n"
                                   "[3] : View orders for a Customer\n"
                                   "[4] : Return to Previous Menu\n"
                                   )
    admin_order_true_list = ["1","2","3","4"]
    admin_order_valid_message = ("Hint: Please re-enter or choose [4] to return"
                                  " to previous menu")
    delete_message = f"{line_break}Delete succesful"
    delete_fail = f"{line_break}Something went wrong!!"
    admin_order_view = ("Please enter customer ID and Page Number and "
                        "seperate with whitespaces"
                        "\n Eg : u_9424171894 1")
    no_orders_message = ("The customer doesnt have any order yet\n")
    admin_order_option_size = 1
    
    IOInterface().print_message(admin_order_option_message)
    
    admin_order_ip = ""
    while True : 
        admin_order_ip = IOInterface().get_user_input(choose_message, 
                                                admin_order_option_size)
        if any ( _ not in admin_order_true_list for _ in admin_order_ip)  :    
            IOInterface().print_message(admin_order_valid_message)
            continue
        else: 
            break
        
    if admin_order_ip[0] == "1" :
        ord_id_list = IOInterface().get_user_input("Enter Order ID", 1)
        del_flag = OrderOperation().delete_order(ord_id_list[0])
        if del_flag : 
            IOInterface().print_message(delete_message)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return run_admin_menu(admin_obj)
        else :
            IOInterface().print_message(delete_fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return run_admin_menu(admin_obj)
            
    if admin_order_ip[0] == "2" : 
        confirm_ip = IOInterface().get_user_input("Press [X] to confirm", 1)
        if confirm_ip[0].lower() == "x" :
            del_flag = OrderOperation().delete_all_orders()
            if del_flag : 
                IOInterface().print_message(delete_message)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return run_admin_menu(admin_obj)
            else :
                IOInterface().print_message(delete_fail)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return run_admin_menu(admin_obj)
    
    if admin_order_ip[0] == "3" :
        ord_id_list = IOInterface().get_user_input(admin_order_view, 2)
        order_disp_tuple = OrderOperation().get_order_list(
            customer_id = ord_id_list[0], 
            page_number = ord_id_list[1])
        order_disp_list = list(order_disp_tuple)
        page_num_invalid_message = ("Invalid page number please choose from 1"
                                    f" to {order_disp_list[2]}")
        if order_disp_list[2] == "0" : 
           IOInterface().print_message(no_orders_message)
           _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
           return admin_order_options(admin_obj)
        
        if len(order_disp_list[0]) == 0 :
            IOInterface().print_message(page_num_invalid_message)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
            return admin_order_options(admin_obj)
        
        IOInterface().show_list(user_role = admin_obj.user_role, 
                                list_type = IOInterface.order_type, 
                                object_list = order_disp_list)
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check, 1)
        return admin_order_options(admin_obj)
        
    if admin_order_ip[0] == "4" : 
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
        return run_admin_menu(admin_obj)
    
#%%
def admin_consumption_options(admin_obj) -> None :
    
    clear_cls()
    header()
    admin_consumption_option_message = ("[1] : Analyse Category Performance\n"
                                        "[2] : Analyse Customer Likes Performance\n"
                                        "[3] : Analyse Discount Performance\n"
                                        "[4] : Analyse Orders Performance\n"
                                        "[5] : Analyse top 10 Performance\n"
                                       "[6] : Return to Previous Menu\n"
                                   )
    admin_consumption_true_list = ["1","2","3","4","5","6"]
    admin_consumption_valid_message = ("Hint: Please re-enter or choose [6] to return"
                                  " to previous menu")
    admin_consumption_option_size = 1
    IOInterface().print_message(admin_consumption_option_message)
    admin_consumption_ip = ""
    while True : 
        admin_consumption_ip = IOInterface().get_user_input(choose_message, 
                                                admin_consumption_option_size)
        if any ( _ not in admin_consumption_true_list for _ in admin_consumption_ip)  :    
            IOInterface().print_message(admin_consumption_valid_message)
            continue
        else: 
            break 
    
    if admin_consumption_ip[0] == "1" : 

        if ProductOperation().generate_category_figure() :
            IOInterface().print_message(graph_sucsess)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
        else : 
            IOInterface().print_message(fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)

    
    if admin_consumption_ip[0] == "2" :
        option = IOInterface().get_user_input(("[1] : Likes across category\n"
                                               "[2] : Likes across discounts\n")
                                               , 1)
        
        if any ( _ not in ["1","2"] for _ in option):
            IOInterface().print_message("\n Wrong input")
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
    
        if option[0] == "1" : 
            if(ProductOperation().generate_likes_count_chart()) : 
                IOInterface().print_message(graph_sucsess)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return admin_consumption_options(admin_obj)
            else : 
                IOInterface().print_message(fail)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return admin_consumption_options(admin_obj)
                
        if option[0] == "2" : 
            if(ProductOperation().generate_likes_discount_scatter()) : 
                IOInterface().print_message(graph_sucsess)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return admin_consumption_options(admin_obj)
            else : 
                IOInterface().print_message(fail)
                _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
                return admin_consumption_options(admin_obj)
            
    
    if admin_consumption_ip[0] == "3" : 
        if ProductOperation().generate_discount_figure() :
            IOInterface().print_message(graph_sucsess)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
        else : 
            IOInterface().print_message(fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
    
    if admin_consumption_ip[0] == "4" : 
        IOInterface().print_message(graph_sucsess)
        if OrderOperation().generate_all_customers_consumption_figure() :
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
        else : 
            IOInterface().print_message(fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)    
    if admin_consumption_ip[0] == "5" : 
        if OrderOperation().generate_all_top_10_best_sellers_figure() :
            IOInterface().print_message(graph_sucsess)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
        else : 
            IOInterface().print_message(fail)
            _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
            return admin_consumption_options(admin_obj)
    if admin_consumption_ip[0] == "6" : 
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
        return run_admin_menu(admin_obj)
                
def admin_generate_test_data(admin_obj) -> None :
    
    test_flag = OrderOperation().generate_test_order_data()
    if test_flag : 
        IOInterface().print_message(f"{line_break}Test data generated successfully!")
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
        return run_admin_menu(admin_obj)
    else : 
        IOInterface().print_message(f"{line_break}Something went wrong!")
        _ = IOInterface().get_user_input(line_break+exit_message_prev_check,1)
        return run_admin_menu(admin_obj)
#%% 

def run_main() -> None :
    
    main_menu_ip_message = choose_message
    main_menu_true_list = ["1","2","3"]
    main_menu_ip_size = 1
    valid_message = "Hint: Please re-enter or choose [3] to exit"
    IOInterface().main_menu()
    
    main_menu_ip = ""
    while True : 
        
        main_menu_ip = IOInterface().get_user_input(main_menu_ip_message, 
                                                main_menu_ip_size)
        if any (ip not in main_menu_true_list for ip in main_menu_ip)  : 
            IOInterface().print_message(valid_message)
            continue
        else : 
            break 
        
    if main_menu_ip[0] == '1' :
        return login_control()
    if main_menu_ip[0] == '2' :
        return customer_profile_control(register)
    if main_menu_ip[0] == "3" :
        return sys.exit()
#%%
def main():
    clear_cls()
    header()
    user_file_check()
    ProductOperation().extract_products_from_files()
    return run_main()
    
        
#%%

if __name__ == "__main__" :     
    main()