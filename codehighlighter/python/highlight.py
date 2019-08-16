# Code Highligher is a LibreOffice extension to highlight code snippets
# over 350 languages.

# Copyright (C) 2017  Gobinath

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pygments import styles
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer
from pygments.styles import get_all_styles
import os


def rgb(r, g, b):
    return (r & 255) << 16 | (g & 255) << 8 | (b & 255)


def to_rgbint(hex_str):
    if hex_str:
        r = int(hex_str[:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:], 16)
        return rgb(r, g, b)
    return rgb(0, 0, 0)


def log(msg, mode='a'):
    with open("/tmp/code-highlighter.log", mode) as text_file:
        text_file.write(str(msg) + "\r\n\r\n")

log('','w')

def create_dialog():
    import uno
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    dialog_m = smgr.createInstance('com.sun.star.awt.UnoControlDialogModel')
    dialog_m.Width = 200
    dialog_m.Height = 100

    label_language = dialog_m.createInstance('com.sun.star.awt.UnoControlFixedTextModel')
    label_language.PositionX = 10
    label_language.PositionY = 30
    label_language.Width  = 100
    label_language.Height = 14
    label_language.Name = 'label_language'
    label_language.TabIndex = 1
    label_language.Label = 'Language: '
    dialog_m.insertByName('label_language', label_language)

    # not showing yet. https://github.com/aberlanas/salt-libreoffice-addon/blob/master/doooLib/doooWindowLib.py
    cb_language_m = dialog_m.createInstance('com.sun.star.awt.UnoControlComboBoxModel')
    cb_language_m.Dropdown = True
    cb_language_m.PositionX = 60
    cb_language_m.PositionY = 30
    cb_language_m.Width  = 100
    cb_language_m.Height = 14
    cb_language_m.Name = 'cb_language_m'
    log(str(dir(cb_language_m)))
    log(str(cb_language_m.StringItemList))
    cb_language_m.Text = 'default'
    cb_language = smgr.createInstance('com.sun.star.awt.UnoControlComboBox')
    cb_language.setModel(cb_language_m)
    cb_language.addItem('l1', 0)
    cb_language.addItem('l2', 1)
    dialog_m.insertByName('cb_language_m', cb_language_m)


    dialog = smgr.createInstance('com.sun.star.awt.UnoControlDialog')
    dialog.setModel(dialog_m)
    dialog.setVisible(True)
    dialog.execute()

def highlightSourceCode(lang, style = 'friendly'):
    create_dialog()
    ctx = XSCRIPTCONTEXT
    doc = ctx.getDocument()
    # Get the selected item
    selected_item = doc.getCurrentController().getSelection()
    if hasattr(selected_item, 'getCount'):
        for item_idx in range(selected_item.getCount()):
            code_block = selected_item.getByIndex(item_idx)
            if 'com.sun.star.drawing.Text' in code_block.SupportedServiceNames:
                # TextBox
                # highlight_code(style, lang, code_block)
                code = code_block.String
                cursor = code_block.createTextCursor()
                cursor.gotoStart(False)
            else:
                # Plain text
                # highlight_code_string(style, lang, code_block)
                code = code_block.getString()
                cursor = code_block.getText().createTextCursorByRange(code_block)
                cursor.goLeft(0, False)
            highlight_code(code, cursor, lang, style)
    elif hasattr(selected_item, 'SupportedServiceNames') and 'com.sun.star.text.TextCursor' in selected_item.SupportedServiceNames:
        # LO Impress text selection
        code_block = selected_item
        code = code_block.getString()
        cursor = code_block.getText().createTextCursorByRange(code_block)
        cursor.goLeft(0, False)
        highlight_code(code, cursor, lang, style)


def highlight_code(code, cursor, lang, style):
    if lang is None:
        lexer = guess_lexer(code)
    else:
        lexer = get_lexer_by_name(lang)
    style = styles.get_style_by_name(style)
    for tok_type, tok_value in lexer.get_tokens(code):
        cursor.goRight(len(tok_value), True)  # selects the token's text
        try:
            cursor.CharColor = to_rgbint(
                style.style_for_token(tok_type)['color'])
        except:
            pass
        finally:
            cursor.goRight(0, False)  # deselects the selected text


def highlight_automatic_default(*args):
    highlightSourceCode(None)

def highlight_automatic_bap(*args):
    highlightSourceCode(None, 'abap')
def highlight_automatic_algol(*args):
    highlightSourceCode(None, 'algol')
def highlight_automatic_algol_nu(*args):
    highlightSourceCode(None, 'algol_nu')
def highlight_automatic_arduino(*args):
    highlightSourceCode(None, 'arduino')
def highlight_automatic_autumn(*args):
    highlightSourceCode(None, 'autumn')
def highlight_automatic_borland(*args):
    highlightSourceCode(None, 'borland')
def highlight_automatic_bw(*args):
    highlightSourceCode(None, 'bw')
def highlight_automatic_colorful(*args):
    highlightSourceCode(None, 'colorful')
def highlight_automatic_emacs(*args):
    highlightSourceCode(None, 'emacs')
def highlight_automatic_friendly(*args):
    highlightSourceCode(None, 'friendly')
def highlight_automatic_fruity(*args):
    highlightSourceCode(None, 'fruity')
def highlight_automatic_igor(*args):
    highlightSourceCode(None, 'igor')
def highlight_automatic_lovelace(*args):
    highlightSourceCode(None, 'lovelace')
def highlight_automatic_manni(*args):
    highlightSourceCode(None, 'manni')
def highlight_automatic_monokai(*args):
    highlightSourceCode(None, 'monokai')
def highlight_automatic_murphy(*args):
    highlightSourceCode(None, 'murphy')
def highlight_automatic_native(*args):
    highlightSourceCode(None, 'native')
def highlight_automatic_paraiso_dark(*args):
    highlightSourceCode(None, 'paraiso-dark')
def highlight_automatic_paraiso_light(*args):
    highlightSourceCode(None, 'paraiso-light')
def highlight_automatic_pastie(*args):
    highlightSourceCode(None, 'pastie')
def highlight_automatic_perldoc(*args):
    highlightSourceCode(None, 'perldoc')
def highlight_automatic_rainbow_dash(*args):
    highlightSourceCode(None, 'rainbow_dash')
def highlight_automatic_rrt(*args):
    highlightSourceCode(None, 'rrt')
def highlight_automatic_tango(*args):
    highlightSourceCode(None, 'tango')
def highlight_automatic_trac(*args):
    highlightSourceCode(None, 'trac')
def highlight_automatic_vim(*args):
    highlightSourceCode(None, 'vim')
def highlight_automatic_vs(*args):
    highlightSourceCode(None, 'vs')
def highlight_automatic_xcode(*args):
    highlightSourceCode(None, 'xcode')

def highlight_abap_default(*args):
    highlightSourceCode('abap')


def highlight_abnf_default(*args):
    highlightSourceCode('abnf')


def highlight_as3_default(*args):
    highlightSourceCode('as3')


def highlight_as_default(*args):
    highlightSourceCode('as')


def highlight_ada_default(*args):
    highlightSourceCode('ada')


def highlight_adl_default(*args):
    highlightSourceCode('adl')


def highlight_agda_default(*args):
    highlightSourceCode('agda')


def highlight_aheui_default(*args):
    highlightSourceCode('aheui')


def highlight_alloy_default(*args):
    highlightSourceCode('alloy')


def highlight_at_default(*args):
    highlightSourceCode('at')


def highlight_ampl_default(*args):
    highlightSourceCode('ampl')


def highlight_ng2_default(*args):
    highlightSourceCode('ng2')


def highlight_antlr_default(*args):
    highlightSourceCode('antlr')


def highlight_apacheconf_default(*args):
    highlightSourceCode('apacheconf')


def highlight_apl_default(*args):
    highlightSourceCode('apl')


def highlight_applescript_default(*args):
    highlightSourceCode('applescript')


def highlight_arduino_default(*args):
    highlightSourceCode('arduino')


def highlight_aspectj_default(*args):
    highlightSourceCode('aspectj')


def highlight_aspx_cs_default(*args):
    highlightSourceCode('aspx-cs')


def highlight_aspx_vb_default(*args):
    highlightSourceCode('aspx-vb')


def highlight_asy_default(*args):
    highlightSourceCode('asy')


def highlight_ahk_default(*args):
    highlightSourceCode('ahk')


def highlight_autoit_default(*args):
    highlightSourceCode('autoit')


def highlight_awk_default(*args):
    highlightSourceCode('awk')


def highlight_basemake_default(*args):
    highlightSourceCode('basemake')


def highlight_console_default(*args):
    highlightSourceCode('console')


def highlight_bash_default(*args):
    highlightSourceCode('bash')


def highlight_bat_default(*args):
    highlightSourceCode('bat')


def highlight_bbcode_default(*args):
    highlightSourceCode('bbcode')


def highlight_bc_default(*args):
    highlightSourceCode('bc')


def highlight_befunge_default(*args):
    highlightSourceCode('befunge')


def highlight_bib_default(*args):
    highlightSourceCode('bib')


def highlight_blitzbasic_default(*args):
    highlightSourceCode('blitzbasic')


def highlight_blitzmax_default(*args):
    highlightSourceCode('blitzmax')


def highlight_bnf_default(*args):
    highlightSourceCode('bnf')


def highlight_boo_default(*args):
    highlightSourceCode('boo')


def highlight_boogie_default(*args):
    highlightSourceCode('boogie')


def highlight_brainfuck_default(*args):
    highlightSourceCode('brainfuck')


def highlight_bro_default(*args):
    highlightSourceCode('bro')


def highlight_bst_default(*args):
    highlightSourceCode('bst')


def highlight_bugs_default(*args):
    highlightSourceCode('bugs')


def highlight_csharp_default(*args):
    highlightSourceCode('csharp')


def highlight_c_objdump_default(*args):
    highlightSourceCode('c-objdump')


def highlight_c_default(*args):
    highlightSourceCode('c')


def highlight_cpp_default(*args):
    highlightSourceCode('cpp')


def highlight_ca65_default(*args):
    highlightSourceCode('ca65')


def highlight_cadl_default(*args):
    highlightSourceCode('cadl')


def highlight_camkes_default(*args):
    highlightSourceCode('camkes')


def highlight_capnp_default(*args):
    highlightSourceCode('capnp')


def highlight_capdl_default(*args):
    highlightSourceCode('capdl')


def highlight_cbmbas_default(*args):
    highlightSourceCode('cbmbas')


def highlight_ceylon_default(*args):
    highlightSourceCode('ceylon')


def highlight_cfengine3_default(*args):
    highlightSourceCode('cfengine3')


def highlight_cfs_default(*args):
    highlightSourceCode('cfs')


def highlight_chai_default(*args):
    highlightSourceCode('chai')


def highlight_chapel_default(*args):
    highlightSourceCode('chapel')


def highlight_cheetah_default(*args):
    highlightSourceCode('cheetah')


def highlight_cirru_default(*args):
    highlightSourceCode('cirru')


def highlight_clay_default(*args):
    highlightSourceCode('clay')


def highlight_clean_default(*args):
    highlightSourceCode('clean')


def highlight_clojure_default(*args):
    highlightSourceCode('clojure')


def highlight_clojurescript_default(*args):
    highlightSourceCode('clojurescript')


def highlight_cmake_default(*args):
    highlightSourceCode('cmake')


def highlight_cobol_default(*args):
    highlightSourceCode('cobol')


def highlight_cobolfree_default(*args):
    highlightSourceCode('cobolfree')


def highlight_coffee_script_default(*args):
    highlightSourceCode('coffee-script')


def highlight_cfc_default(*args):
    highlightSourceCode('cfc')


def highlight_cfm_default(*args):
    highlightSourceCode('cfm')


def highlight_common_lisp_default(*args):
    highlightSourceCode('common-lisp')


def highlight_componentpascal_default(*args):
    highlightSourceCode('componentpascal')


def highlight_coq_default(*args):
    highlightSourceCode('coq')


def highlight_cpp_objdump_default(*args):
    highlightSourceCode('cpp-objdump')


def highlight_cpsa_default(*args):
    highlightSourceCode('cpsa')


def highlight_crmsh_default(*args):
    highlightSourceCode('crmsh')


def highlight_croc_default(*args):
    highlightSourceCode('croc')


def highlight_cryptol_default(*args):
    highlightSourceCode('cryptol')


def highlight_cr_default(*args):
    highlightSourceCode('cr')


def highlight_csound_document_default(*args):
    highlightSourceCode('csound-document')


def highlight_csound_default(*args):
    highlightSourceCode('csound')


def highlight_csound_score_default(*args):
    highlightSourceCode('csound-score')


def highlight_css_default(*args):
    highlightSourceCode('css')


def highlight_cuda_default(*args):
    highlightSourceCode('cuda')


def highlight_cypher_default(*args):
    highlightSourceCode('cypher')


def highlight_cython_default(*args):
    highlightSourceCode('cython')


def highlight_d_objdump_default(*args):
    highlightSourceCode('d-objdump')


def highlight_d_default(*args):
    highlightSourceCode('d')


def highlight_dpatch_default(*args):
    highlightSourceCode('dpatch')


def highlight_dart_default(*args):
    highlightSourceCode('dart')


def highlight_control_default(*args):
    highlightSourceCode('control')


def highlight_sourceslist_default(*args):
    highlightSourceCode('sourceslist')


def highlight_delphi_default(*args):
    highlightSourceCode('delphi')


def highlight_dg_default(*args):
    highlightSourceCode('dg')


def highlight_diff_default(*args):
    highlightSourceCode('diff')


def highlight_django_default(*args):
    highlightSourceCode('django')


def highlight_docker_default(*args):
    highlightSourceCode('docker')


def highlight_dtd_default(*args):
    highlightSourceCode('dtd')


def highlight_duel_default(*args):
    highlightSourceCode('duel')


def highlight_dylan_console_default(*args):
    highlightSourceCode('dylan-console')


def highlight_dylan_default(*args):
    highlightSourceCode('dylan')


def highlight_dylan_lid_default(*args):
    highlightSourceCode('dylan-lid')


def highlight_earl_grey_default(*args):
    highlightSourceCode('earl-grey')


def highlight_easytrieve_default(*args):
    highlightSourceCode('easytrieve')


def highlight_ebnf_default(*args):
    highlightSourceCode('ebnf')


def highlight_ec_default(*args):
    highlightSourceCode('ec')


def highlight_ecl_default(*args):
    highlightSourceCode('ecl')


def highlight_eiffel_default(*args):
    highlightSourceCode('eiffel')


def highlight_iex_default(*args):
    highlightSourceCode('iex')


def highlight_elixir_default(*args):
    highlightSourceCode('elixir')


def highlight_elm_default(*args):
    highlightSourceCode('elm')


def highlight_emacs_default(*args):
    highlightSourceCode('emacs')


def highlight_ragel_em_default(*args):
    highlightSourceCode('ragel-em')


def highlight_erb_default(*args):
    highlightSourceCode('erb')


def highlight_erl_default(*args):
    highlightSourceCode('erl')


def highlight_erlang_default(*args):
    highlightSourceCode('erlang')


def highlight_evoque_default(*args):
    highlightSourceCode('evoque')


def highlight_ezhil_default(*args):
    highlightSourceCode('ezhil')


def highlight_factor_default(*args):
    highlightSourceCode('factor')


def highlight_fancy_default(*args):
    highlightSourceCode('fancy')


def highlight_fan_default(*args):
    highlightSourceCode('fan')


def highlight_felix_default(*args):
    highlightSourceCode('felix')


def highlight_fish_default(*args):
    highlightSourceCode('fish')


def highlight_flatline_default(*args):
    highlightSourceCode('flatline')


def highlight_forth_default(*args):
    highlightSourceCode('forth')


def highlight_fortran_default(*args):
    highlightSourceCode('fortran')


def highlight_fortranfixed_default(*args):
    highlightSourceCode('fortranfixed')


def highlight_foxpro_default(*args):
    highlightSourceCode('foxpro')


def highlight_fsharp_default(*args):
    highlightSourceCode('fsharp')


def highlight_gap_default(*args):
    highlightSourceCode('gap')


def highlight_gas_default(*args):
    highlightSourceCode('gas')


def highlight_genshitext_default(*args):
    highlightSourceCode('genshitext')


def highlight_genshi_default(*args):
    highlightSourceCode('genshi')


def highlight_pot_default(*args):
    highlightSourceCode('pot')


def highlight_cucumber_default(*args):
    highlightSourceCode('cucumber')


def highlight_glsl_default(*args):
    highlightSourceCode('glsl')


def highlight_gnuplot_default(*args):
    highlightSourceCode('gnuplot')


def highlight_go_default(*args):
    highlightSourceCode('go')


def highlight_golo_default(*args):
    highlightSourceCode('golo')


def highlight_gooddata_cl_default(*args):
    highlightSourceCode('gooddata-cl')


def highlight_gst_default(*args):
    highlightSourceCode('gst')


def highlight_gosu_default(*args):
    highlightSourceCode('gosu')


def highlight_groff_default(*args):
    highlightSourceCode('groff')


def highlight_groovy_default(*args):
    highlightSourceCode('groovy')


def highlight_haml_default(*args):
    highlightSourceCode('haml')


def highlight_handlebars_default(*args):
    highlightSourceCode('handlebars')


def highlight_haskell_default(*args):
    highlightSourceCode('haskell')


def highlight_hx_default(*args):
    highlightSourceCode('hx')


def highlight_hexdump_default(*args):
    highlightSourceCode('hexdump')


def highlight_hsail_default(*args):
    highlightSourceCode('hsail')


def highlight_html_default(*args):
    highlightSourceCode('html')


def highlight_http_default(*args):
    highlightSourceCode('http')


def highlight_haxeml_default(*args):
    highlightSourceCode('haxeml')


def highlight_hylang_default(*args):
    highlightSourceCode('hylang')


def highlight_hybris_default(*args):
    highlightSourceCode('hybris')


def highlight_idl_default(*args):
    highlightSourceCode('idl')


def highlight_idris_default(*args):
    highlightSourceCode('idris')


def highlight_igor_default(*args):
    highlightSourceCode('igor')


def highlight_i6t_default(*args):
    highlightSourceCode('i6t')


def highlight_inform6_default(*args):
    highlightSourceCode('inform6')


def highlight_inform7_default(*args):
    highlightSourceCode('inform7')


def highlight_ini_default(*args):
    highlightSourceCode('ini')


def highlight_io_default(*args):
    highlightSourceCode('io')


def highlight_ioke_default(*args):
    highlightSourceCode('ioke')


def highlight_irc_default(*args):
    highlightSourceCode('irc')


def highlight_isabelle_default(*args):
    highlightSourceCode('isabelle')


def highlight_j_default(*args):
    highlightSourceCode('j')


def highlight_jags_default(*args):
    highlightSourceCode('jags')


def highlight_jasmin_default(*args):
    highlightSourceCode('jasmin')


def highlight_jsp_default(*args):
    highlightSourceCode('jsp')


def highlight_java_default(*args):
    highlightSourceCode('java')


def highlight_js_default(*args):
    highlightSourceCode('js')


def highlight_jcl_default(*args):
    highlightSourceCode('jcl')


def highlight_jsgf_default(*args):
    highlightSourceCode('jsgf')


def highlight_jsonld_default(*args):
    highlightSourceCode('jsonld')


def highlight_json_default(*args):
    highlightSourceCode('json')


def highlight_json_object_default(*args):
    highlightSourceCode('json-object')


def highlight_jlcon_default(*args):
    highlightSourceCode('jlcon')


def highlight_julia_default(*args):
    highlightSourceCode('julia')


def highlight_juttle_default(*args):
    highlightSourceCode('juttle')


def highlight_kal_default(*args):
    highlightSourceCode('kal')


def highlight_kconfig_default(*args):
    highlightSourceCode('kconfig')


def highlight_koka_default(*args):
    highlightSourceCode('koka')


def highlight_kotlin_default(*args):
    highlightSourceCode('kotlin')


def highlight_lasso_default(*args):
    highlightSourceCode('lasso')


def highlight_lean_default(*args):
    highlightSourceCode('lean')


def highlight_less_default(*args):
    highlightSourceCode('less')


def highlight_lighty_default(*args):
    highlightSourceCode('lighty')


def highlight_limbo_default(*args):
    highlightSourceCode('limbo')


def highlight_liquid_default(*args):
    highlightSourceCode('liquid')


def highlight_lagda_default(*args):
    highlightSourceCode('lagda')


def highlight_lcry_default(*args):
    highlightSourceCode('lcry')


def highlight_lhs_default(*args):
    highlightSourceCode('lhs')


def highlight_lidr_default(*args):
    highlightSourceCode('lidr')


def highlight_live_script_default(*args):
    highlightSourceCode('live-script')


def highlight_llvm_default(*args):
    highlightSourceCode('llvm')


def highlight_logos_default(*args):
    highlightSourceCode('logos')


def highlight_logtalk_default(*args):
    highlightSourceCode('logtalk')


def highlight_lsl_default(*args):
    highlightSourceCode('lsl')


def highlight_lua_default(*args):
    highlightSourceCode('lua')


def highlight_make_default(*args):
    highlightSourceCode('make')


def highlight_mako_default(*args):
    highlightSourceCode('mako')


def highlight_maql_default(*args):
    highlightSourceCode('maql')


def highlight_md_default(*args):
    highlightSourceCode('md')


def highlight_mask_default(*args):
    highlightSourceCode('mask')


def highlight_mason_default(*args):
    highlightSourceCode('mason')


def highlight_mathematica_default(*args):
    highlightSourceCode('mathematica')


def highlight_matlabsession_default(*args):
    highlightSourceCode('matlabsession')


def highlight_matlab_default(*args):
    highlightSourceCode('matlab')


def highlight_minid_default(*args):
    highlightSourceCode('minid')


def highlight_modelica_default(*args):
    highlightSourceCode('modelica')


def highlight_modula2_default(*args):
    highlightSourceCode('modula2')


def highlight_trac_wiki_default(*args):
    highlightSourceCode('trac-wiki')


def highlight_monkey_default(*args):
    highlightSourceCode('monkey')


def highlight_monte_default(*args):
    highlightSourceCode('monte')


def highlight_moocode_default(*args):
    highlightSourceCode('moocode')


def highlight_moon_default(*args):
    highlightSourceCode('moon')


def highlight_mozhashpreproc_default(*args):
    highlightSourceCode('mozhashpreproc')


def highlight_mozpercentpreproc_default(*args):
    highlightSourceCode('mozpercentpreproc')


def highlight_mql_default(*args):
    highlightSourceCode('mql')


def highlight_mscgen_default(*args):
    highlightSourceCode('mscgen')


def highlight_doscon_default(*args):
    highlightSourceCode('doscon')


def highlight_mupad_default(*args):
    highlightSourceCode('mupad')


def highlight_mxml_default(*args):
    highlightSourceCode('mxml')


def highlight_myghty_default(*args):
    highlightSourceCode('myghty')


def highlight_mysql_default(*args):
    highlightSourceCode('mysql')


def highlight_nasm_default(*args):
    highlightSourceCode('nasm')


def highlight_ncl_default(*args):
    highlightSourceCode('ncl')


def highlight_nemerle_default(*args):
    highlightSourceCode('nemerle')


def highlight_nesc_default(*args):
    highlightSourceCode('nesc')


def highlight_newlisp_default(*args):
    highlightSourceCode('newlisp')


def highlight_newspeak_default(*args):
    highlightSourceCode('newspeak')


def highlight_nginx_default(*args):
    highlightSourceCode('nginx')


def highlight_nim_default(*args):
    highlightSourceCode('nim')


def highlight_nit_default(*args):
    highlightSourceCode('nit')


def highlight_nixos_default(*args):
    highlightSourceCode('nixos')


def highlight_nsis_default(*args):
    highlightSourceCode('nsis')


def highlight_numpy_default(*args):
    highlightSourceCode('numpy')


def highlight_nusmv_default(*args):
    highlightSourceCode('nusmv')


def highlight_objdump_nasm_default(*args):
    highlightSourceCode('objdump-nasm')


def highlight_objdump_default(*args):
    highlightSourceCode('objdump')


def highlight_objective_c_default(*args):
    highlightSourceCode('objective-c')


def highlight_objective_j_default(*args):
    highlightSourceCode('objective-j')


def highlight_ocaml_default(*args):
    highlightSourceCode('ocaml')


def highlight_octave_default(*args):
    highlightSourceCode('octave')


def highlight_odin_default(*args):
    highlightSourceCode('odin')


def highlight_ooc_default(*args):
    highlightSourceCode('ooc')


def highlight_opa_default(*args):
    highlightSourceCode('opa')


def highlight_openedge_default(*args):
    highlightSourceCode('openedge')


def highlight_pacmanconf_default(*args):
    highlightSourceCode('pacmanconf')


def highlight_pan_default(*args):
    highlightSourceCode('pan')


def highlight_parasail_default(*args):
    highlightSourceCode('parasail')


def highlight_pawn_default(*args):
    highlightSourceCode('pawn')


def highlight_perl6_default(*args):
    highlightSourceCode('perl6')


def highlight_perl_default(*args):
    highlightSourceCode('perl')


def highlight_php_default(*args):
    highlightSourceCode('php')


def highlight_pig_default(*args):
    highlightSourceCode('pig')


def highlight_pike_default(*args):
    highlightSourceCode('pike')


def highlight_pkgconfig_default(*args):
    highlightSourceCode('pkgconfig')


def highlight_plpgsql_default(*args):
    highlightSourceCode('plpgsql')


def highlight_psql_default(*args):
    highlightSourceCode('psql')


def highlight_postgresql_default(*args):
    highlightSourceCode('postgresql')


def highlight_postscript_default(*args):
    highlightSourceCode('postscript')


def highlight_pov_default(*args):
    highlightSourceCode('pov')


def highlight_ps1con_default(*args):
    highlightSourceCode('ps1con')


def highlight_powershell_default(*args):
    highlightSourceCode('powershell')


def highlight_praat_default(*args):
    highlightSourceCode('praat')


def highlight_prolog_default(*args):
    highlightSourceCode('prolog')


def highlight_properties_default(*args):
    highlightSourceCode('properties')


def highlight_protobuf_default(*args):
    highlightSourceCode('protobuf')


def highlight_pug_default(*args):
    highlightSourceCode('pug')


def highlight_puppet_default(*args):
    highlightSourceCode('puppet')


def highlight_pypylog_default(*args):
    highlightSourceCode('pypylog')


def highlight_py3tb_default(*args):
    highlightSourceCode('py3tb')


def highlight_python3_default(*args):
    highlightSourceCode('python3')


def highlight_pycon_default(*args):
    highlightSourceCode('pycon')


def highlight_pytb_default(*args):
    highlightSourceCode('pytb')


def highlight_python_default(*args):
    highlightSourceCode('python')


def highlight_qbasic_default(*args):
    highlightSourceCode('qbasic')


def highlight_qml_default(*args):
    highlightSourceCode('qml')


def highlight_qvto_default(*args):
    highlightSourceCode('qvto')


def highlight_racket_default(*args):
    highlightSourceCode('racket')


def highlight_ragel_c_default(*args):
    highlightSourceCode('ragel-c')


def highlight_ragel_cpp_default(*args):
    highlightSourceCode('ragel-cpp')


def highlight_ragel_d_default(*args):
    highlightSourceCode('ragel-d')


def highlight_ragel_java_default(*args):
    highlightSourceCode('ragel-java')


def highlight_ragel_objc_default(*args):
    highlightSourceCode('ragel-objc')


def highlight_ragel_ruby_default(*args):
    highlightSourceCode('ragel-ruby')


def highlight_ragel_default(*args):
    highlightSourceCode('ragel')


def highlight_rconsole_default(*args):
    highlightSourceCode('rconsole')


def highlight_rd_default(*args):
    highlightSourceCode('rd')


def highlight_rebol_default(*args):
    highlightSourceCode('rebol')


def highlight_red_default(*args):
    highlightSourceCode('red')


def highlight_redcode_default(*args):
    highlightSourceCode('redcode')


def highlight_registry_default(*args):
    highlightSourceCode('registry')


def highlight_rnc_default(*args):
    highlightSourceCode('rnc')


def highlight_resource_default(*args):
    highlightSourceCode('resource')


def highlight_rst_default(*args):
    highlightSourceCode('rst')


def highlight_rexx_default(*args):
    highlightSourceCode('rexx')


def highlight_rhtml_default(*args):
    highlightSourceCode('rhtml')


def highlight_roboconf_graph_default(*args):
    highlightSourceCode('roboconf-graph')


def highlight_roboconf_instances_default(*args):
    highlightSourceCode('roboconf-instances')


def highlight_robotframework_default(*args):
    highlightSourceCode('robotframework')


def highlight_spec_default(*args):
    highlightSourceCode('spec')


def highlight_rql_default(*args):
    highlightSourceCode('rql')


def highlight_rsl_default(*args):
    highlightSourceCode('rsl')


def highlight_rbcon_default(*args):
    highlightSourceCode('rbcon')


def highlight_rb_default(*args):
    highlightSourceCode('rb')


def highlight_rust_default(*args):
    highlightSourceCode('rust')


def highlight_splus_default(*args):
    highlightSourceCode('splus')


def highlight_sas_default(*args):
    highlightSourceCode('sas')


def highlight_sass_default(*args):
    highlightSourceCode('sass')


def highlight_scala_default(*args):
    highlightSourceCode('scala')


def highlight_ssp_default(*args):
    highlightSourceCode('ssp')


def highlight_scaml_default(*args):
    highlightSourceCode('scaml')


def highlight_scheme_default(*args):
    highlightSourceCode('scheme')


def highlight_scilab_default(*args):
    highlightSourceCode('scilab')


def highlight_scss_default(*args):
    highlightSourceCode('scss')


def highlight_shen_default(*args):
    highlightSourceCode('shen')


def highlight_silver_default(*args):
    highlightSourceCode('silver')


def highlight_slim_default(*args):
    highlightSourceCode('slim')


def highlight_smali_default(*args):
    highlightSourceCode('smali')


def highlight_smalltalk_default(*args):
    highlightSourceCode('smalltalk')


def highlight_smarty_default(*args):
    highlightSourceCode('smarty')


def highlight_snobol_default(*args):
    highlightSourceCode('snobol')


def highlight_snowball_default(*args):
    highlightSourceCode('snowball')


def highlight_sp_default(*args):
    highlightSourceCode('sp')


def highlight_sparql_default(*args):
    highlightSourceCode('sparql')


def highlight_sql_default(*args):
    highlightSourceCode('sql')


def highlight_sqlite3_default(*args):
    highlightSourceCode('sqlite3')


def highlight_squidconf_default(*args):
    highlightSourceCode('squidconf')


def highlight_stan_default(*args):
    highlightSourceCode('stan')


def highlight_sml_default(*args):
    highlightSourceCode('sml')


def highlight_stata_default(*args):
    highlightSourceCode('stata')


def highlight_sc_default(*args):
    highlightSourceCode('sc')


def highlight_swift_default(*args):
    highlightSourceCode('swift')


def highlight_swig_default(*args):
    highlightSourceCode('swig')


def highlight_systemverilog_default(*args):
    highlightSourceCode('systemverilog')


def highlight_tads3_default(*args):
    highlightSourceCode('tads3')


def highlight_tap_default(*args):
    highlightSourceCode('tap')


def highlight_tasm_default(*args):
    highlightSourceCode('tasm')


def highlight_tcl_default(*args):
    highlightSourceCode('tcl')


def highlight_tcshcon_default(*args):
    highlightSourceCode('tcshcon')


def highlight_tcsh_default(*args):
    highlightSourceCode('tcsh')


def highlight_tea_default(*args):
    highlightSourceCode('tea')


def highlight_termcap_default(*args):
    highlightSourceCode('termcap')


def highlight_terminfo_default(*args):
    highlightSourceCode('terminfo')


def highlight_terraform_default(*args):
    highlightSourceCode('terraform')


def highlight_tex_default(*args):
    highlightSourceCode('tex')


def highlight_text_default(*args):
    highlightSourceCode('text')


def highlight_thrift_default(*args):
    highlightSourceCode('thrift')


def highlight_todotxt_default(*args):
    highlightSourceCode('todotxt')


def highlight_rts_default(*args):
    highlightSourceCode('rts')


def highlight_tsql_default(*args):
    highlightSourceCode('tsql')


def highlight_treetop_default(*args):
    highlightSourceCode('treetop')


def highlight_turtle_default(*args):
    highlightSourceCode('turtle')


def highlight_twig_default(*args):
    highlightSourceCode('twig')


def highlight_ts_default(*args):
    highlightSourceCode('ts')


def highlight_typoscript_default(*args):
    highlightSourceCode('typoscript')


def highlight_typoscriptcssdata_default(*args):
    highlightSourceCode('typoscriptcssdata')


def highlight_typoscripthtmldata_default(*args):
    highlightSourceCode('typoscripthtmldata')


def highlight_urbiscript_default(*args):
    highlightSourceCode('urbiscript')


def highlight_vala_default(*args):
    highlightSourceCode('vala')


def highlight_vb_net_default(*args):
    highlightSourceCode('vb.net')


def highlight_vcl_default(*args):
    highlightSourceCode('vcl')


def highlight_vclsnippets_default(*args):
    highlightSourceCode('vclsnippets')


def highlight_vctreestatus_default(*args):
    highlightSourceCode('vctreestatus')


def highlight_velocity_default(*args):
    highlightSourceCode('velocity')


def highlight_verilog_default(*args):
    highlightSourceCode('verilog')


def highlight_vgl_default(*args):
    highlightSourceCode('vgl')


def highlight_vhdl_default(*args):
    highlightSourceCode('vhdl')


def highlight_vim_default(*args):
    highlightSourceCode('vim')


def highlight_wdiff_default(*args):
    highlightSourceCode('wdiff')


def highlight_whiley_default(*args):
    highlightSourceCode('whiley')


def highlight_x10_default(*args):
    highlightSourceCode('x10')


def highlight_xml_default(*args):
    highlightSourceCode('xml')


def highlight_xquery_default(*args):
    highlightSourceCode('xquery')


def highlight_xslt_default(*args):
    highlightSourceCode('xslt')


def highlight_xtend_default(*args):
    highlightSourceCode('xtend')


def highlight_extempore_default(*args):
    highlightSourceCode('extempore')


def highlight_yaml_default(*args):
    highlightSourceCode('yaml')


def highlight_zephir_default(*args):
    highlightSourceCode('zephir')


g_exportedScripts = (highlight_abap_default, highlight_abnf_default, highlight_as3_default, highlight_as_default, highlight_ada_default, highlight_adl_default, highlight_agda_default, highlight_aheui_default, highlight_alloy_default, highlight_at_default, highlight_ampl_default, highlight_ng2_default, highlight_antlr_default, highlight_apacheconf_default, highlight_apl_default, highlight_applescript_default, highlight_arduino_default, highlight_aspectj_default, highlight_aspx_cs_default, highlight_aspx_vb_default, highlight_asy_default, highlight_ahk_default, highlight_autoit_default, highlight_awk_default, highlight_basemake_default, highlight_console_default, highlight_bash_default, highlight_bat_default, highlight_bbcode_default, highlight_bc_default, highlight_befunge_default, highlight_bib_default, highlight_blitzbasic_default, highlight_blitzmax_default, highlight_bnf_default, highlight_boo_default, highlight_boogie_default, highlight_brainfuck_default, highlight_bro_default, highlight_bst_default, highlight_bugs_default, highlight_csharp_default, highlight_c_objdump_default, highlight_c_default, highlight_cpp_default, highlight_ca65_default, highlight_cadl_default, highlight_camkes_default, highlight_capnp_default, highlight_capdl_default, highlight_cbmbas_default, highlight_ceylon_default, highlight_cfengine3_default, highlight_cfs_default, highlight_chai_default, highlight_chapel_default, highlight_cheetah_default, highlight_cirru_default, highlight_clay_default, highlight_clean_default, highlight_clojure_default, highlight_clojurescript_default, highlight_cmake_default, highlight_cobol_default, highlight_cobolfree_default, highlight_coffee_script_default, highlight_cfc_default, highlight_cfm_default, highlight_common_lisp_default, highlight_componentpascal_default, highlight_coq_default, highlight_cpp_objdump_default, highlight_cpsa_default, highlight_crmsh_default, highlight_croc_default, highlight_cryptol_default, highlight_cr_default, highlight_csound_document_default, highlight_csound_default, highlight_csound_score_default, highlight_css_default, highlight_cuda_default, highlight_cypher_default, highlight_cython_default, highlight_d_objdump_default, highlight_d_default, highlight_dpatch_default, highlight_dart_default, highlight_control_default, highlight_sourceslist_default, highlight_delphi_default, highlight_dg_default, highlight_diff_default, highlight_django_default, highlight_docker_default, highlight_dtd_default, highlight_duel_default, highlight_dylan_console_default, highlight_dylan_default, highlight_dylan_lid_default, highlight_earl_grey_default, highlight_easytrieve_default, highlight_ebnf_default, highlight_ec_default, highlight_ecl_default, highlight_eiffel_default, highlight_iex_default, highlight_elixir_default, highlight_elm_default, highlight_emacs_default, highlight_ragel_em_default, highlight_erb_default, highlight_erl_default, highlight_erlang_default, highlight_evoque_default, highlight_ezhil_default, highlight_factor_default, highlight_fancy_default, highlight_fan_default, highlight_felix_default, highlight_fish_default, highlight_flatline_default, highlight_forth_default, highlight_fortran_default, highlight_fortranfixed_default, highlight_foxpro_default, highlight_fsharp_default, highlight_gap_default, highlight_gas_default, highlight_genshitext_default, highlight_genshi_default, highlight_pot_default, highlight_cucumber_default, highlight_glsl_default, highlight_gnuplot_default, highlight_go_default, highlight_golo_default, highlight_gooddata_cl_default, highlight_gst_default, highlight_gosu_default, highlight_groff_default, highlight_groovy_default, highlight_haml_default, highlight_handlebars_default, highlight_haskell_default, highlight_hx_default, highlight_hexdump_default, highlight_hsail_default, highlight_html_default, highlight_http_default, highlight_haxeml_default, highlight_hylang_default, highlight_hybris_default, highlight_idl_default, highlight_idris_default, highlight_igor_default, highlight_i6t_default, highlight_inform6_default, highlight_inform7_default, highlight_ini_default, highlight_io_default, highlight_ioke_default, highlight_irc_default, highlight_isabelle_default, highlight_j_default, highlight_jags_default, highlight_jasmin_default, highlight_jsp_default, highlight_java_default, highlight_js_default, highlight_jcl_default, highlight_jsgf_default, highlight_jsonld_default, highlight_json_default, highlight_json_object_default, highlight_jlcon_default, highlight_julia_default, highlight_juttle_default, highlight_kal_default, highlight_kconfig_default, highlight_koka_default, highlight_kotlin_default, highlight_lasso_default, highlight_lean_default, highlight_less_default, highlight_lighty_default, highlight_limbo_default, highlight_liquid_default, highlight_lagda_default, highlight_lcry_default, highlight_lhs_default, highlight_lidr_default,
                     highlight_live_script_default, highlight_llvm_default, highlight_logos_default, highlight_logtalk_default, highlight_lsl_default, highlight_lua_default, highlight_make_default, highlight_mako_default, highlight_maql_default, highlight_md_default, highlight_mask_default, highlight_mason_default, highlight_mathematica_default, highlight_matlabsession_default, highlight_matlab_default, highlight_minid_default, highlight_modelica_default, highlight_modula2_default, highlight_trac_wiki_default, highlight_monkey_default, highlight_monte_default, highlight_moocode_default, highlight_moon_default, highlight_mozhashpreproc_default, highlight_mozpercentpreproc_default, highlight_mql_default, highlight_mscgen_default, highlight_doscon_default, highlight_mupad_default, highlight_mxml_default, highlight_myghty_default, highlight_mysql_default, highlight_nasm_default, highlight_ncl_default, highlight_nemerle_default, highlight_nesc_default, highlight_newlisp_default, highlight_newspeak_default, highlight_nginx_default, highlight_nim_default, highlight_nit_default, highlight_nixos_default, highlight_nsis_default, highlight_numpy_default, highlight_nusmv_default, highlight_objdump_nasm_default, highlight_objdump_default, highlight_objective_c_default, highlight_objective_j_default, highlight_ocaml_default, highlight_octave_default, highlight_odin_default, highlight_ooc_default, highlight_opa_default, highlight_openedge_default, highlight_pacmanconf_default, highlight_pan_default, highlight_parasail_default, highlight_pawn_default, highlight_perl6_default, highlight_perl_default, highlight_php_default, highlight_pig_default, highlight_pike_default, highlight_pkgconfig_default, highlight_plpgsql_default, highlight_psql_default, highlight_postgresql_default, highlight_postscript_default, highlight_pov_default, highlight_ps1con_default, highlight_powershell_default, highlight_praat_default, highlight_prolog_default, highlight_properties_default, highlight_protobuf_default, highlight_pug_default, highlight_puppet_default, highlight_pypylog_default, highlight_py3tb_default, highlight_python3_default, highlight_pycon_default, highlight_pytb_default, highlight_python_default, highlight_qbasic_default, highlight_qml_default, highlight_qvto_default, highlight_racket_default, highlight_ragel_c_default, highlight_ragel_cpp_default, highlight_ragel_d_default, highlight_ragel_java_default, highlight_ragel_objc_default, highlight_ragel_ruby_default, highlight_ragel_default, highlight_rconsole_default, highlight_rd_default, highlight_rebol_default, highlight_red_default, highlight_redcode_default, highlight_registry_default, highlight_rnc_default, highlight_resource_default, highlight_rst_default, highlight_rexx_default, highlight_rhtml_default, highlight_roboconf_graph_default, highlight_roboconf_instances_default, highlight_robotframework_default, highlight_spec_default, highlight_rql_default, highlight_rsl_default, highlight_rbcon_default, highlight_rb_default, highlight_rust_default, highlight_splus_default, highlight_sas_default, highlight_sass_default, highlight_scala_default, highlight_ssp_default, highlight_scaml_default, highlight_scheme_default, highlight_scilab_default, highlight_scss_default, highlight_shen_default, highlight_silver_default, highlight_slim_default, highlight_smali_default, highlight_smalltalk_default, highlight_smarty_default, highlight_snobol_default, highlight_snowball_default, highlight_sp_default, highlight_sparql_default, highlight_sql_default, highlight_sqlite3_default, highlight_squidconf_default, highlight_stan_default, highlight_sml_default, highlight_stata_default, highlight_sc_default, highlight_swift_default, highlight_swig_default, highlight_systemverilog_default, highlight_tads3_default, highlight_tap_default, highlight_tasm_default, highlight_tcl_default, highlight_tcshcon_default, highlight_tcsh_default, highlight_tea_default, highlight_termcap_default, highlight_terminfo_default, highlight_terraform_default, highlight_tex_default, highlight_text_default, highlight_thrift_default, highlight_todotxt_default, highlight_rts_default, highlight_tsql_default, highlight_treetop_default, highlight_turtle_default, highlight_twig_default, highlight_ts_default, highlight_typoscript_default, highlight_typoscriptcssdata_default, highlight_typoscripthtmldata_default, highlight_urbiscript_default, highlight_vala_default, highlight_vb_net_default, highlight_vcl_default, highlight_vclsnippets_default, highlight_vctreestatus_default, highlight_velocity_default, highlight_verilog_default, highlight_vgl_default, highlight_vhdl_default, highlight_vim_default, highlight_wdiff_default, highlight_whiley_default, highlight_x10_default, highlight_xml_default, highlight_xquery_default, highlight_xslt_default, highlight_xtend_default, highlight_extempore_default, highlight_yaml_default, highlight_zephir_default,)
