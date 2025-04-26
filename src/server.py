import MolDisplay
import molsql
import molecule
import urllib
import io
from http.server import HTTPServer,BaseHTTPRequestHandler

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path in ['/', '/resources/styles.css', '/resources/scripts.js', '/resources/display.html', '/resources/form.html']:
            self.send_response(200)

            if self.path == '/':
                self.path = '/index.html'

            fp = open(self.path[1:])
            page = fp.read()
            fp.close()

            if self.path == '/resources/styles.css':
                self.send_header("content-type", "text/css")
            elif self.path == '/resources/scripts.js':
                self.send_header("content-type", "text/javascript")
            else:
                self.send_header("content-type", "text/html")
            self.send_header("content-length", len(page))
            self.end_headers()

            self.wfile.write(bytes(page, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: not found", "utf-8" ) )

    def do_POST(self):
        #upload
        if self.path == "/molecule":
            content_length = int(self.headers['Content-Length'])

            try:
                info = self.rfile.read(content_length)
                data = urllib.parse.parse_qs(info.decode('utf-8'))

                mol_name = urllib.parse.unquote(data[' name'][0]).splitlines()
                mol_name = mol_name[2]
                file = urllib.parse.unquote(data[' filename'][0]).splitlines()
                file = file[3:]

                db.add_molecule(mol_name, io.StringIO('\n'.join(file)))
                try :
                    mol = db.load_mol(mol_name)
                    mol.sort()

                    MolDisplay.radius = db.radius()
                    MolDisplay.element_name = db.element_name()
                    MolDisplay.header += db.radial_gradients()

                    display = mol.svg()
                    self.send_response(200)
                except:
                    self.send_response(400)
                    display = "Incorrect file format"
            except KeyError:
                self.send_response(400)
                display = "Input is empty"
            except:
                self.send_response(400)
                display = "Incorrect File type"
            finally:
                self.send_header("content-type", "text/plain")
                self.send_header("content-length", len(display))
                self.end_headers()

                self.wfile.write(bytes(display, "utf-8"))
                MolDisplay.header = """<svg version="1.1" width="1000" height="1000"
                xmlns="http://www.w3.org/2000/svg">"""
        #add element
        elif self.path == "/element":
            content_length = int(self.headers['Content-Length'])
            info = self.rfile.read(content_length)

            mol_info = urllib.parse.parse_qs( info.decode( 'utf-8' ) )
            try:
                db['Elements'] = (int(mol_info["number"][0]), mol_info["code"][0], mol_info["name"][0], mol_info["colour1"][0], mol_info["colour2"][0], mol_info["colour3"][0], int(mol_info["radius"][0]))
                self.send_response(200)
                display = "Received"
            except KeyError:
                self.send_response(400)
                display = "Empty input"
            except:
                self.send_response(400)
                display = "Error - Element in the system"


            self.send_header("content-type", "text/plain")
            self.send_header("content-length", len(display))
            self.end_headers()

            self.wfile.write(bytes(display, "utf-8"))
        #display list of molecules
        elif self.path == "/displayList":
            mol_names = db.get_molecule_names()
            output = """"""
            for mol in mol_names:
                output += """<input type="radio" id="{}" name="options" onclick="displayMol($(this))">
                          <label for="{}">{}</label><br>""".format(mol[0], mol[0], mol[0])

            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", len(output))
            self.end_headers()

            self.wfile.write(bytes(output, "utf-8"))
        elif self.path == "/displayElements":
            element_names = db.get_element_names()
            output = """"""
            for element in element_names:
                output += """<label>{}</label><button class="rightBtn" id="{}"
                    onclick="rmElement($(this))">Remove</button><br><br>""".format(element[0], element[0])

            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.send_header("content-length", len(output))
            self.end_headers()

            self.wfile.write(bytes(output, "utf-8"))

        elif self.path == "/rmElement":
            content_length = int(self.headers['Content-Length'])
            info = self.rfile.read(content_length)
            element_name = urllib.parse.unquote(info.decode('utf-8'))

            try:
                db.remove_element(element_name)
                display = "Removed successfully"
                self.send_response(200)
            except:
                display = "Element in the system"
                self.send_response(400)

            self.send_header("content-type", "plain/text")
            self.send_header("content-length", len(display))
            self.end_headers()

            self.wfile.write(bytes(display, "utf-8"))

        elif self.path == "/rotation":
            content_length = int(self.headers['Content-Length'])
            info = self.rfile.read(content_length)

            mol_info = urllib.parse.parse_qs( info.decode('utf-8'))
            try:
                mol = db.load_mol(mol_info["name"][0])
                try:
                    if int(mol_info["xrot"][0]) > 0:
                        mx = molecule.mx_wrapper(int(mol_info["xrot"][0]),0,0)
                        mol.xform(mx.xform_matrix)

                    if int(mol_info["yrot"][0]) > 0:
                        mx = molecule.mx_wrapper(0,int(mol_info["yrot"][0]),0)
                        mol.xform(mx.xform_matrix)

                    if int(mol_info["zrot"][0]) > 0:
                        mx = molecule.mx_wrapper(0,0,int(mol_info["zrot"][0]))
                        mol.xform(mx.xform_matrix)
                    mol.sort()

                    MolDisplay.radius = db.radius()
                    MolDisplay.element_name = db.element_name()
                    MolDisplay.header += db.radial_gradients()

                    display = mol.svg()
                    self.send_response(200)
                except:
                    display = "Error - Empty text boxes"
                    self.send_response(400)
            except:
                display = "Error - no selected molecule"
                self.send_response(400)

            self.send_header("content-type", "plain/text")
            self.send_header("content-length", len(display))
            self.end_headers()

            self.wfile.write(bytes(display, "utf-8"))
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000"
            xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/displayMol":
            content_length = int(self.headers['Content-Length'])
            info = self.rfile.read(content_length)
            molname = urllib.parse.unquote(info.decode('utf-8'))
            print(molname)
            mol = db.load_mol(molname)
            mol.sort()

            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()

            display = mol.svg()

            self.send_response(200)
            self.send_header("content-type", "image/svg")
            self.send_header("content-length", len(display))
            self.end_headers()

            self.wfile.write(bytes(display, "utf-8"))
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000"
            xmlns="http://www.w3.org/2000/svg">"""
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes( "404: not found", "utf-8" ))


db = molsql.Database(False)
httpd = HTTPServer( ( 'localhost', 57455 ), myHandler )
httpd.serve_forever()
