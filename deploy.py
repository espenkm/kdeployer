import os
import yaml
import jinja2
import uuid
import base64

from kubernetes import client, config
from kubernetes.client.rest import ApiException

pretty ='pretty_example'
conflict = 409
namespace = "default"

def replace_function(api, type):
    return getattr(api, "patch_namespaced_" + type)

def create_function(api, type):
    return getattr(api, "create_namespaced_" + type)

def get_or_create_secret(name):
    k8s = client.CoreV1Api()

    try:
        k8s_secret = k8s.read_namespaced_secret(name, namespace)
        secret = base64.b64decode(k8s_secret.data['password'])
    except ApiException as e:
        secret = uuid.uuid4()

        data = []
        data["password"] = base64.b64encode(secret)
        k8s.create_namespaced_secret(namespace, client.V1Secret(name=name, namespace=namespace, data=data))

    return secret

def create_or_update_certificate(context):
    k8s_custom = client.CustomObjectsApi()
    dep = load_file("certificate", context)

    try:
        api_response = k8s_custom.create_cluster_custom_object("certmanager.k8s.io", "v1alpha1", "", dep, pretty=pretty)
        print(api_response)
    except ApiException as e:
        if e.status == conflict:
            resp = k8s_custom.patch_cluster_custom_object("certmanager.k8s.io", "v1alpha1",  "", dep, pretty=pretty)
            print("%s updated. status='%s'", type_name, str(resp.status))
        else:
            raise e

def create_or_update(api, type_name,  namespace, context):
    dep = load_file(type_name, context)
    try:
        resp = create_function(api, type_name)(body=dep, namespace=namespace)
        print("%s created. status='%s'", type_name, str(resp.status))
    except ApiException as e:
        if e.status == conflict:
            resp = replace_function(api, type_name)(
                name=context["name"], body=dep, namespace=namespace, pretty=pretty)
            print("%s updated. status='%s'", type_name, str(resp.status))
        else:
            raise e

def load_file(name, context):
    return yaml.load(render(name, context))

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path + ".yaml")
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './config/')
    ).get_template(filename).render(context)

def update_k8s(context):
    host = context["name"]
    if context["env"] != "prod":
        host += "." + context["env"]
    host += "." + context["domain"]

    context["host"] = host
    print(context)

    load_config()

    k8s = client.CoreV1Api()
    k8s_beta = client.ExtensionsV1beta1Api()

    create_or_update_certificate(namespace, context)
    create_or_update(k8s, "service", namespace, context)
    create_or_update(k8s_beta, "ingress", namespace, context)
    create_or_update(k8s_beta, "deployment", namespace, context)

def load_config():
    if ("KUBERNETES_SERVICE_HOST" in os.environ):
        config.load_incluster_config()
    elif ("KUBECONFIG" in os.environ):
        config.load_kube_config(os.environ.get("KUBECONFIG"))
    else:
        config.load_kube_config()


def main():
    with open(".kdeploy.yaml") as context:
        update_k8s(yaml.load(context))

if __name__ == '__main__':
    main()
