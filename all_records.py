import gradio
from mongodb_connect import fetchAllRecords


def generateTabularRecords(output):
    records = fetchAllRecords()
    for record in records:
        output = output + "<tr>"
        id = record["_id"]
        try:
            name = record['Key Points']['basics']['name'][0]
        except:
            name = "N.A."
        phone = record['Key Points']['basics']['phone']
        email = record['Key Points']['basics']['email']
        companies = record['Key Points']['work']['company']
        positions = record['Key Points']['work']['position']
        locations = record['Key Points']['basics']['location']
        languages = record['Key Points']['basics']['language']
        skills = record['Key Points']['expertise']['skill']
        phone, email, languages, locations = [
            "-" if not data else data for data in (phone, email, languages, locations)]
        output = output + \
            f'<td><a style="color:yellow" href="/applicant/{id}">{id}</a></td><td>{name}</td><td>{ ", ".join(map(str, phone))}</td><td>{ ", ".join(map(str, email))}</td><td>{ ", ".join(map(str, companies))}</td><td>{ ", ".join(map(str, positions))}</td><td>{ ", ".join(map(str, locations))}</td><td>{ ", ".join(map(str, languages))}</td><td>{ ", ".join(map(str, skills))}</td></tr>'
    output = output + "</tbody></table></body></html>"
    return output


with gradio.Blocks(theme=gradio.themes.Monochrome(), title="Applicant Records") as block:
    with open("./templates/records.html", "r") as file:
        table = file.read()
    table = generateTabularRecords(table)
    gradio.HTML(table)
