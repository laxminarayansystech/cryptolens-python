# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 08:06:39 2019

@author: Artem Los
"""

import platform
import uuid
import sys
from licensing.internal import HelperMethods
from licensing.models import *
import json
from urllib.error import URLError, HTTPError

class Key:
    
    """
    License key related methods. More docs: https://app.cryptolens.io/docs/api/v3/Key.
    """
    
    @staticmethod
    def activate(token, rsa_pub_key, product_id, key, machine_code, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0,\
                 max_overdraft = 0, friendly_name = None):
        
        """
        Calls the Activate method in Web API 3 and returns a tuple containing
        (LicenseKey, Message). If an error occurs, LicenseKey will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Activate
        """
        
        response = Response("","",0,"")
        
        try:
            response = Response.from_string(HelperMethods.send_request("key/activate", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "key":key,\
                                                  "MachineCode":machine_code,\
                                                  "FieldsToReturn":fields_to_return,\
                                                  "metadata":metadata,\
                                                  "FloatingTimeInterval": floating_time_interval,\
                                                  "MaxOverdraft": max_overdraft,\
                                                  "FriendlyName" : friendly_name,\
                                                  "ModelVersion": 2 ,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        pubkey = RSAPublicKey.from_string(rsa_pub_key)
    
        if response.result == 1:
            return (None, response.message)
        else:
            try:
                if HelperMethods.verify_signature(response, pubkey):
                    return (LicenseKey.from_response(response), response.message)
                else:
                    return (None, "The signature check failed.")
            except Exception:
                return (None, "The signature check failed.")
            
    @staticmethod
    def get_key(token, rsa_pub_key, product_id, key, fields_to_return = 0,\
                 metadata = False, floating_time_interval = 0):
        
        """
        Calls the GetKey method in Web API 3 and returns a tuple containing
        (LicenseKey, Message). If an error occurs, LicenseKey will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetKey
        """
        
        response = Response("","",0,"")
        
        try:
            response = Response.from_string(HelperMethods.send_request("key/getkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "key":key,\
                                                  "FieldsToReturn":fields_to_return,\
                                                  "metadata":metadata,\
                                                  "FloatingTimeInterval": floating_time_interval,\
                                                  "Sign":"True",\
                                                  "SignMethod":1}))
        except HTTPError as e:
            response = Response.from_string(e.read())
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        pubkey = RSAPublicKey.from_string(rsa_pub_key)
    
        if response.result == 1:
            return (None, response.message)
        else:
            try:
                if HelperMethods.verify_signature(response, pubkey):
                    return (LicenseKey.from_response(response), response.message)
                else:
                    return (None, "The signature check failed.")
            except Exception:
                return (None, "The signature check failed.")
     
    @staticmethod
    def create_trial_key(token, product_id, machine_code):
        """
        Calls the CreateTrialKey method in Web API 3 and returns a tuple containing
        (LicenseKeyString, Message). If an error occurs, LicenseKeyString will be None. If
        everything went well, no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateTrialKey
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/createtrialkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "MachineCode":machine_code})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")
           
        return (jobj["key"], "")
    
    @staticmethod
    def create_key(token, product_id, period = 0,\
                   f1=False,\
                   f2=False,\
                   f3=False,\
                   f4=False,\
                   f5=False,\
                   f6=False,\
                   f7=False,\
                   f8=False,\
                   notes="",\
                   block=False,\
                   customer_id=0,\
                   new_customer=False,\
                   add_or_use_existing_customer=False,\
                   trial_activation=False,\
                   max_no_of_machines=0,\
                   no_of_keys=1):
        """
        This method allows you to create a new license key. The license can
        either be standalone or associated to a specific customer. It is also
        possible to add a new customer and associate it with the newly created
        license using NewCustomer parameter. If you would like to avoid
        duplicates based on the email, you can use the AddOrUseExistingCustomer
        parameter.
        
        More docs: https://app.cryptolens.io/docs/api/v3/CreateKey/
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/createkey", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Period":period,\
                                                  "F1": f1,\
                                                  "F2": f2,\
                                                  "F3": f3,\
                                                  "F4": f4,\
                                                  "F5": f5,\
                                                  "F6": f6,\
                                                  "F7": f7,\
                                                  "F8": f8,\
                                                  "Notes": notes,\
                                                  "Block": block,\
                                                  "CustomerId": customer_id,\
                                                  "NewCustomer": new_customer,\
                                                  "AddOrUseExistingCustomer": add_or_use_existing_customer,\
                                                  "TrialActivation": trial_activation,\
                                                  "MaxNoOfMachines": max_no_of_machines,\
                                                  "NoOfKeys":no_of_keys})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")
           
        return (jobj, "")
    
    
    @staticmethod
    def deactivate(token, product_id, key, machine_code, floating = False):
        """
        Calls the Deactivate method in Web API 3 and returns a tuple containing
        (Success, Message). If an error occurs, Success will be False. If
        everything went well, Sucess is true and no message will be returned.
        
        More docs: https://app.cryptolens.io/docs/api/v3/Deactivate
        """
        
        response = ""
        
        try:
            response = HelperMethods.send_request("key/deactivate", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key" : key,\
                                                  "Floating" : floating,\
                                                  "MachineCode":machine_code})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (False, jobj["message"])
            else:
               return (False, "Could not contact the server.")
           
        return (True, "")

    @staticmethod
    def get_web_api_log(token, product_id = 0, key = "", machine_code="", friendly_name = "",\
                        limit = 10, starting_after = 0, ending_before=0, order_by=""):
        
        """
        This method will retrieve a list of Web API Logs. All events that get
        logged are related to a change of a license key or data object, eg. when
        license key gets activated or when a property of data object changes. More details
        about the method that was called are specified in the State field.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetWebAPILog
        """
        
        response = ""
                
        try:
            response = HelperMethods.send_request("ai/getwebapilog", {"token":token,\
                                                  "ProductId":product_id,\
                                                  "Key":key,\
                                                  "MachineCode":machine_code,\
                                                  "FriendlyName":friendly_name,\
                                                  "Limit": limit,\
                                                  "StartingAfter": starting_after,\
                                                  "OrderBy" : order_by,\
                                                  "EndingBefore": ending_before})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")
        
        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")
           
        return (jobj["logs"], "")
            
class Message:
    
    @staticmethod
    def get_messages(token, channel="", time=0):
        
        """
        This method will return a list of messages that were broadcasted.
        You can create new messages here. Messages can be filtered based on the time and the channel.
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetMessages
        """
        
        try:
            response = HelperMethods.send_request("/message/getmessages/", {"token":token, "Channel": channel, "Time": time})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")

        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")

        return (jobj["messages"], "")
    
    
class Product:
    
    @staticmethod
    def get_products(token):
        
        """
        This method will return the list of products. Each product contains fields such as
        the name and description, as well feature definitions and data objects. All the fields
        of a product are available here: https://app.cryptolens.io/docs/api/v3/model/Product
        
        More docs: https://app.cryptolens.io/docs/api/v3/GetProducts
        """
        
        try:
            response = HelperMethods.send_request("/product/getproducts/", {"token":token})
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")

        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")

        return (jobj["products"], "")
    
    
class Customer:
    
    @staticmethod
    def add_customer(token, name = "", email = "", company_name="",\
                     enable_customer_association = False,\
                     allow_activation_management = False ):
        
        """
        This method will add new customer.
        
        More docs: https://app.cryptolens.io/docs/api/v3/AddCustomer
        """
        
        try:
            response = HelperMethods.send_request("/customer/addcustomer/",\
                                                  {"token":token,\
                                                   "Name": name,\
                                                   "Email": email,\
                                                   "CompanyName": company_name,\
                                                   "EnableCustomerAssociation": enable_customer_association,\
                                                   "AllowActivationManagement": allow_activation_management
                                                   })
        except HTTPError as e:
            response = e.read()
        except URLError as e:
            return (None, "Could not contact the server. Error message: " + str(e))
        except Exception:
            return (None, "Could not contact the server.")

        jobj = json.loads(response)

        if jobj == None or not("result" in jobj) or jobj["result"] == 1:
            if jobj != None:
                return (None, jobj["message"])
            else:
               return (None, "Could not contact the server.")

        return (jobj, "")
            
class Helpers:
    
    @staticmethod
    def GetMachineCode(v=1):
        
        """
        Get a unique identifier for this device. If you want the machine code to be the same in .NET on Windows, you
        can set v=2. More information is available here: https://help.cryptolens.io/faq/index#machine-code-generation
        """
        
        if "windows" in platform.platform().lower():
            return HelperMethods.get_SHA256(HelperMethods.start_process(["cmd.exe", "/C", "wmic","csproduct", "get", "uuid"],v))
        elif "mac" in platform.platform().lower() or "darwin" in platform.platform().lower():               
            res = HelperMethods.start_process(["system_profiler","SPHardwareDataType"])
            return HelperMethods.get_SHA256(res[res.index("UUID"):].strip())
        elif "linux" in platform.platform().lower() :
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
        else:
            return HelperMethods.get_SHA256(HelperMethods.compute_machine_code())
    
    @staticmethod
    def IsOnRightMachine(license_key, is_floating_license = False, allow_overdraft=False, v = 1):
        
        """
        Check if the device is registered with the license key.
        The version parameter is related to the one in GetMachineCode method.
        """
        
        current_mid = Helpers.GetMachineCode(v)
        
        if license_key.activated_machines == None:
            return False
        
        if is_floating_license:
            if len(license_key.activated_machines) == 1 and \
            (license_key.activated_machines[0].Mid[9:] == current_mid or \
             allow_overdraft and license_key.activated_machines[0].Mid[19:] == current_mid):
                return True
        else:
            for act_machine in license_key.activated_machines:
                if current_mid == act_machine.Mid:
                    return True
            
        return False
