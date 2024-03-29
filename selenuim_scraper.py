from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from matplotlib import pyplot as plt
#import discord_msg_sender as disc

def plot_results(color_list):
    num_of_color = {"red": 0, "black": 0, "white": 0}
    for element in color_list:
        if element == "red":
            num_of_color["red"] += 1
        if element == "black":
            num_of_color["black"] += 1
        if element == "white":
            num_of_color["white"] += 1


    plt.style.use("fivethirtyeight")
    total_colors_picked = len(color_list)
    for i in range(2):
        if list(num_of_color.values())[i]/total_colors_picked > 0.5:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'g')
        elif list(num_of_color.values())[i]/total_colors_picked < 0.5:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'r')
        else:
            plt.bar(list(num_of_color.keys())[i], list(num_of_color.values())[i], color = 'b')

    if list(num_of_color.values())[2]/total_colors_picked > (1/14):
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'g')
    elif list(num_of_color.values())[2]/total_colors_picked < 0.5:
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'r')
    else:
        plt.bar(list(num_of_color.keys())[2], list(num_of_color.values())[2], color = 'b')


    plt.ylabel("quantity selected")
    plt.xlabel("total_colors_picked = {} " .format(total_colors_picked))
    plt.title("Blaze Double results")
    plt.show()


def play_double(color_list):
    
    print("how much money do you want to play with?")
    your_money = int(input())

    for i in range(len(color_list)):

        if your_money == 0:
            break

        chosen_color = input("pick a color (red, black or white)")

        print("place a bet")
        bet = int(input())
        print("\n")

        while bet > your_money:
            print("insufficient funds, try again")
            print("place a bet")
            bet = int(input())
            print("\n")

        if chosen_color == "white":
            if color_list[i] == chosen_color:
                print("the winning color is " + color_list[i])
                print("well done!")
                your_money += bet*13
                print("now you have {} dollars\n\n" .format(your_money))
            else:
                print("the winning color is " + color_list[i])
                print("better luck next time")
                your_money -= bet
                print("now you have {} dollars\n\n" .format(your_money))
        else:
            if str(color_list[i]) == chosen_color:
                print("the winning color is " + color_list[i])
                print("well done!")
                your_money += bet
                print("now you have {} dollars\n\n" .format(your_money))
            else:
                print("the winning color is " + color_list[i])
                print("better luck next time")
                your_money -= bet
                print("now you have {} dollars\n\n" .format(your_money))

    print("now you have {} dollars" .format(your_money))


def write_to_txt(color_list, file_name):
    with open(file_name, "w") as file:
        for color in color_list:
            file.write(color)
            file.write("\n")


############################ VARIABLES YOU MAY WANT TO CHANGE #############################
max_len_dict = 10000  # number of rounds that will be evaluated
number_of_rounds_whitout_white = 85 # will start betting on white after this amount of rounds without white
number_of_rounds_before_white = 45 # cheacks how many whites have been selected in the past "number_of_rounds_before_white" rounds
number_of_bets_after_white = 10 # after a white has been selected will continue betting on white for this number of rounds if its worth it
betting_money = "2" # Will bet this quantity on white
###########################################################################################

dictionary = {}
investo_counter = 0
message_counter = 0
the_colors = []
seed_before_click = " "
your_money = []

website = "https://blaze.com/en/games/double?modal=double_history_index"
website2 = "https://blaze.com/en/games/double?modal=auth&tab=login"

email = input("Enter your Blaze acount email")
password = input("Enter your password")


options = ChromeOptions()
options.add_experimental_option("detach", True)

driver = Chrome(service=Service(ChromeDriverManager().install()), options=options) 

driver2 = Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(website)
driver2.get(website2)

driver2.find_element(By.NAME,"username").send_keys(email)
driver2.find_element(By.NAME,"password").send_keys(password)
WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "input-footer"))).click()

WebDriverWait(driver2, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "input-field")))
driver2.find_element(By.CLASS_NAME, "input-field").send_keys(betting_money)
driver2.find_element(By.CLASS_NAME, "white").click()

while(len(dictionary) < max_len_dict):
    selected_seeds = []
    selected_colors = []

    # Keeps trying to load page with the past 10 selected colors and their identifiers until no issues arise
    num_of_retries = 5
    for x in range(0, num_of_retries):
        try:
            driver.refresh()
            sleep(1)
            # Waits for selected colors to load into page
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, ".//tbody/tr/td[3]/div/a")))
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, ".//tbody/tr/td[2]/div/div")))

            # Gets slected colors and their identifiers from webpage
            selected_seeds = driver.find_elements(By.XPATH, ".//tbody/tr/td[3]/div/a")     
            selected_colors = driver.find_elements(By.XPATH, ".//tbody/tr/td[2]/div/div") 
        except:
            print("TimeoutError occurred: reloding page...")

    # Cleans up data and makes sure same color hasnt been stored twice in dictionary
    for i in range(9,-1, -1):
        seed = selected_seeds[i].text
        _, color = selected_colors[i].get_attribute('class').split(" ")

        if seed not in dictionary:
            dictionary[seed] = color

    # Converts dictionary into 2 lists for ease of use
    the_colors = list(dictionary.values())
    the_seeds = list(dictionary.keys())

    last_seed = the_seeds[-1]

    # Will bet of white if the number of rounds without white chosen has benn surpased
    if len(dictionary) > number_of_rounds_whitout_white and "white" not in the_colors[-number_of_rounds_whitout_white:]:
        if seed_before_click != last_seed:
            sleep(1)
            WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "place-bet"))).click()
            seed_before_click = the_seeds[-1]
            #disc.send_discord_msg(f"Its a Good time to bet! There have been {number_of_rounds_whitout_white + message_counter} rounds without white")
            message_counter += 1
            print("entered situation 1")

    # Checks for how many whites have been selected in the last "number_of_round_before_white" rounds
    num_of_whites = the_colors[-number_of_rounds_before_white:].count("white") #number_of_rounds_whitout_white

    # If the last color selected is white, bets on white again
    if list(the_colors)[-1] == "white" and num_of_whites < 2 and len(dictionary) > number_of_rounds_before_white:
        if seed_before_click != last_seed:
            sleep(1)
            WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "place-bet"))).click()
            seed_before_click = the_seeds[-1]
            investo_counter = 1
            message_counter = 0
            print("entered situation 2")


    # After a white token has been selected continues betting on white for a set amount of rounds
    if investo_counter > 0 and num_of_whites < 2:
        if investo_counter >= number_of_bets_after_white:
            investo_counter = 0

        if seed_before_click != last_seed:
            sleep(0.5)
            WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "place-bet"))).click()
            seed_before_click = the_seeds[-1]
            investo_counter += 1
            print("entered situation 3")


    if num_of_whites >= 2:
        investo_counter = 0

    # Stores data to .txt file for data analysis
    x = driver2.find_element(By.CLASS_NAME, "currency").get_attribute("textContent")
    your_money.append(x)
    write_to_txt(your_money, "money.txt")
    write_to_txt(the_colors, "selected_colors.txt")


# plot_results(the_colors)

# play_double(the_colors)

driver.quit()
driver2.quit()
