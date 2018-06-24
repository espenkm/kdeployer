import os
import yaml
import jinja2

from kubernetes import client, config
from kubernetes.client.rest import ApiException

pretty ='pretty_example'
conflict = 409
namespace = "default"

def delete_function(api, type):
    return getattr(api, "delete_namespaced_" + type)

def replace_function(api, type):
    return getattr(api, "replace_namespaced_" + type)

def create_function(api, type):
    return getattr(api, "create_namespaced_" + type)

def create_or_recreate(api, type_name, context):
    dep = load_file(type_name, context)
    try:
        resp = create_function(api, type_name)(body=dep, namespace=namespace)
        print("%s created. status='%s'", type_name, str(resp.status))
    except ApiException as e:
        if e.status == conflict:
            resp = delete_function(api, type_name)(name=context["name"],namespace=namespace, pretty=pretty)
            print("%s deleted. status='%s'", type_name, str(resp.status))

            resp = create_function(api, type_name)(body=dep, namespace=namespace, pretty=pretty)
            print("%s updated. status='%s'", type_name, str(resp.status))
        else:
            raise e

def create_or_update(api, type_name,  context):
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
    print(context)

    load_config()

    k8s = client.CoreV1Api()
    k8s_beta = client.ExtensionsV1beta1Api()

    create_or_recreate(k8s, "service", context)
    create_or_update(k8s_beta, "custom_resource_definition	", context)
    create_or_update(k8s_beta, "deployment", context)

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
