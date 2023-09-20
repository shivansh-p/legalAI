from tkinter import *
import markdown
import markdownify
import createAbe
import webbrowser
import os
DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    text = '''# Summary of User Rights and Privileges Relating to Smoking Cannabis

## Rights and Privileges
According to California law, a user who is 21 years or older has the right to possess, process, transport, purchase, obtain, or give away up to 28.5 grams of cannabis not in the form of concentrated cannabis, or up to eight grams of cannabis in the form of concentrated cannabis. They can also cultivate up to six living cannabis plants and possess the cannabis produced by those plants. They are allowed to smoke or ingest cannabis or cannabis products and possess, transport, purchase, obtain, use, manufacture, or give away cannabis accessories to persons 21 years of age or older without any compensation (Cal. HSC § 11362.1). 

Users also have the right to consume nonmedical marijuana if they are over 21 years of age and in compliance with California law and any applicable local standards, requirements, and regulations (Cal. CIV § 1550.5). They have the right to use cannabis off the job and away from the workplace without facing discrimination in hiring, termination, or any term or condition of employment based on that use (Cal. GOV § 12954). 

## Restrictions
However, there are restrictions on these rights. Users cannot smoke or ingest cannabis in public places, where smoking tobacco is prohibited, within 1,000 feet of a school, day care center, or youth center while children are present, or in or upon the grounds of a school, day care center, or youth center while children are present. They also cannot possess an open container or package of cannabis or cannabis products while operating a vehicle or transportation vehicle, and cannot smoke or ingest cannabis or cannabis products while driving or riding in a vehicle used for transportation (Cal. HSC § 11362.3). 

Users also cannot smoke cannabis while driving or operating a vehicle, boat, vessel, or aircraft, on the grounds of certain facilities or institutions, and on the property of a state or local government agency or on privately owned property where it is prohibited or restricted (Cal. HSC § 11362.45). 

## Local Jurisdiction Regulations
User rights and privileges relating to smoking cannabis can also depend on the local jurisdiction's regulations. Local jurisdictions have the authority to adopt and enforce ordinances to regulate businesses licensed under this division, including regulations related to reducing exposure to secondhand smoke (Cal. BPC § 26200). 

## Medical Cannabis
For medical cannabis users, they have the right to transport, process, administer, deliver, or give away cannabis for medical purposes if they are a qualified patient, a person with an identification card, or a designated primary caregiver (Cal. HSC § 11362.765). They may also request the court to confirm their right to use cannabis while on probation or released on bail (Cal. HSC § 11362.795). 

## Limitations
However, users do not have the right or privilege to smoke or vape cannabis in a health care facility (Cal. HSC § 1649.2). They also cannot smoke medicinal cannabis in a place where smoking is prohibited by law, in or within 1,000 feet of the grounds of a school, recreation center, or youth center, unless the medicinal use occurs within a residence, on a school bus, while in a motor vehicle that is being operated, or while operating a boat (Cal. HSC § 11362.79). 

## Cultivation
Users also have the right to cultivate and possess cannabis for personal use, but there are certain restrictions that apply. The cultivation of cannabis must comply with local ordinances, if any, and must be done within the person's private residence or on the grounds of that private residence in a locked space that is not visible from a public place (Cal. HSC § 11362.2). 

## Other Rights
Users also have the right to have cannabis or cannabis products tested by a licensed testing laboratory for quality control purposes (Cal. BPC § 26104). They can also purchase and possess cannabis or cannabis products if they are 21 years of age or older (Cal. BPC § 26140). 

## Conclusion
In conclusion, while users have certain rights and privileges relating to smoking cannabis, there are also restrictions and limitations on these rights. These rights and privileges can also be regulated by local ordinances.
    '''
    markdown_to_html(text)

def markdown_to_html(text):
    print("HERE!")
    html_string = markdown.markdown(text)
    with open("sample.html","w") as html_file:
        html_file.write(html_string)
    html_file.close()
    open_html_in_browser("sample.html")



def open_html_in_browser(file_name):
    new = 2 # open in a new tab, if possible

    # open a public URL, in this case, the webbrowser docs

    # open an HTML file on my own (Windows) computer
    url = "file://{}/{}".format(DIR, file_name)
    webbrowser.open(url,new=new)

if __name__ == "__main__":
    main()